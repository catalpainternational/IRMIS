import hashlib
import json
import pytz
import reversion
from reversion.models import Version
from datetime import datetime
from collections import Counter
import pytz

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    JsonResponse,
    HttpResponseNotFound,
)
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.exceptions import MethodNotAllowed, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_condition import condition

from google.protobuf.timestamp_pb2 import Timestamp

from protobuf import roads_pb2, survey_pb2


from .models import (
    CollatedGeoJsonFile,
    Road,
    MaintenanceNeed,
    TechnicalClass,
    RoadStatus,
    SurfaceType,
    PavementClass,
    Survey,
)
from .serializers import (
    RoadSerializer,
    RoadMetaOnlySerializer,
    RoadToWGSSerializer,
    SurveySerializer,
)


def get_etag(request, pk=None):
    try:
        if pk:
            return hashlib.md5(
                json.dumps(
                    RoadSerializer(Road.objects.filter(id=pk).get()).data
                ).encode("utf-8")
            ).hexdigest()
        else:
            return hashlib.md5(
                json.dumps(RoadSerializer(Road.objects.all(), many=True).data).encode(
                    "utf-8"
                )
            ).hexdigest()
    except Road.DoesNotExist:
        return hashlib.md5(json.dumps({}).encode("utf-8")).hexdigest()


def get_last_modified(request, pk=None):
    try:
        if pk:
            return Road.objects.filter(id=pk).latest("last_modified").last_modified
        else:
            return Road.objects.all().latest("last_modified").last_modified
    except Road.DoesNotExist:
        return datetime.now()


class RoadViewSet(ViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @condition(etag_func=get_etag, last_modified_func=get_last_modified)
    def list(self, request):
        queryset = Road.objects.all()
        serializer = RoadMetaOnlySerializer(queryset, many=True)
        return Response(serializer.data)

    @condition(etag_func=get_etag, last_modified_func=get_last_modified)
    def retrieve(self, request, pk):
        # Allow metadata retrival for single road with param: `?meta`
        if "meta" in request.query_params:
            queryset = Road.objects.all()
            road = get_object_or_404(queryset, pk=pk)
            serializer = RoadMetaOnlySerializer(road)
            return Response(serializer.data)
        else:
            queryset = Road.objects.to_wgs()
            road = get_object_or_404(queryset, pk=pk)
            serializer = RoadToWGSSerializer(road)
            return Response(serializer.data)

    def create(self, request):
        raise MethodNotAllowed(request.method)

    def destroy(self, request, pk):
        raise MethodNotAllowed(request.method)


def road_update(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    if request.method != "PUT":
        raise MethodNotAllowed(request.method)
    elif request.content_type != "application/octet-stream":
        return HttpResponse(status=400)

    # parse Road from protobuf in request body
    req_pb = roads_pb2.Road()
    req_pb.ParseFromString(request.body)

    # check that Protobuf parsed
    if not req_pb.id:
        return HttpResponse(status=400)

    # assert Road ID given exists in the DB & there are changes to make
    road = get_object_or_404(Road.objects.filter(pk=req_pb.id))
    old_road_pb = Road.objects.filter(pk=req_pb.id).to_protobuf().roads[0]
    if old_road_pb == req_pb:
        response = HttpResponse(
            req_pb.SerializeToString(),
            status=200,
            content_type="application/octet-stream",
        )
        return response

    # check if the Road has revision history, then check if Road
    # edits would be overwriting someone's changes
    version = Version.objects.get_for_object(road).first()
    if version and req_pb.last_revision_id != version.revision.id:
        return HttpResponse(status=409)

    # update the Road instance from PB fields
    fields = [
        "road_name",
        "road_code",
        "road_type",
        "link_code",
        "link_start_name",
        "link_start_chainage",
        "link_end_name",
        "link_end_chainage",
        "link_length",
        "surface_condition",
        "carriageway_width",
        "administrative_area",
        "project",
        "funding_source",
        "traffic_level",
    ]
    fks = [
        (MaintenanceNeed, "maintenance_need"),
        (TechnicalClass, "technical_class"),
        (RoadStatus, "road_status"),
        (SurfaceType, "surface_type"),
        (PavementClass, "pavement_class"),
    ]
    changed_fields = []
    for field in fields:
        request_value = getattr(req_pb, field)
        if getattr(old_road_pb, field) != request_value:
            # set attribute on road
            setattr(road, field, request_value)
            # add field to list of changes fields
            changed_fields.append(field)

    # Foreign Key attributes
    for fk in fks:
        field = fk[1]
        model = fk[0]
        request_value = getattr(req_pb, field, None)
        if getattr(old_road_pb, field) != request_value:
            if request_value:
                try:
                    fk_obj = model.objects.filter(code=request_value).get()
                except model.DoesNotExist:
                    return HttpResponse(status=400)
            else:
                fk_obj = None
            setattr(road, field, fk_obj)
            # add field to list of changes fields
            changed_fields.append(field)

    with reversion.create_revision():
        road.save()

        # store the user who made the changes
        reversion.set_user(request.user)

        # construct a django admin log style change message and use that
        # to create a revision comment and an admin log entry
        change_message = [dict(changed=dict(fields=changed_fields))]
        reversion.set_comment(json.dumps(change_message))
        LogEntry.objects.log_action(
            request.user.id,
            ContentType.objects.get_for_model(Road).pk,
            road.pk,
            str(road),
            CHANGE,
            change_message,
        )

    versions = Version.objects.get_for_object(road)
    req_pb.last_revision_id = versions[0].id

    response = HttpResponse(
        req_pb.SerializeToString(), status=200, content_type="application/octet-stream"
    )
    return response


def geojson_details(request):
    """ returns a JSON object with details of geoJSON geometry collections """

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    geojson_files = CollatedGeoJsonFile.objects.values("id", "geobuf_file")

    return JsonResponse(list(geojson_files), safe=False)


def protobuf_road(request, pk):
    """ returns an protobuf serialized bytestring with the set of all chunks that can be requested via protobuf_roads """

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    roads = Road.objects.filter(pk=pk)
    if not roads.exists():
        return HttpResponseNotFound()

    roads_protobuf = roads.to_protobuf()

    return HttpResponse(
        roads_protobuf.roads[0].SerializeToString(),
        content_type="application/octet-stream",
    )


def road_chunks_set(request):
    """ returns an object with the set of all chunks that can be requested via protobuf_roads """

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    road_chunks = Road.objects.to_chunks()

    return JsonResponse(list(road_chunks), safe=False)


def protobuf_road_set(request, chunk_name=None):
    """ returns a protobuf object with the set of all Roads """

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    roads = Road.objects.all()
    if chunk_name:
        roads = roads.filter(road_type=chunk_name)

    roads_protobuf = roads.to_protobuf()

    return HttpResponse(
        roads_protobuf.SerializeToString(), content_type="application/octet-stream"
    )


def road_report(request, road_code, rpt_start=0.0, rpt_end=None):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    if request.method != "GET":
        raise MethodNotAllowed(request.method)

    surveys = (
        Survey.objects.filter(road=road_code)
        .order_by("road", "chainage_start", "chainage_end", "-date_surveyed")
        .distinct("road", "chainage_start", "chainage_end")
    )
    report_protobuf = Report(road_code, surveys, rpt_start, rpt_end).to_protobuf()

    return HttpResponse(
        report_protobuf.SerializeToString(), content_type="application/octet-stream"
    )


class Report:
    def __init__(self, road_code, surveys, rpt_start, rpt_end):
        self.road_code = road_code
        try:
            self.road_start_chainage = (
                Road.objects.filter(road_code=road_code)
                .order_by("link_start_chainage")[0]
                .link_start_chainage
            )
            self.road_end_chainage = (
                Road.objects.filter(road_code=road_code)
                .order_by("-link_end_chainage")[0]
                .link_end_chainage
            )
        except IndexError as err:
            raise IndexError("Road Code given did not return any records")

        if len(surveys) > 0:
            self.surveys = surveys
        else:
            raise ValueError("At least one Survey must be provided to build the Report")

        # perform various checks to ensure all start/end chainages are valid
        # and fall within a given Road's chainage range
        self.rpt_start = (
            self.road_start_chainage
        )  # set to Road start chainage initially
        if rpt_start >= self.road_end_chainage:
            raise ValueError(
                "Report Start Chainage given is greater than Road's ending chainage"
            )
        elif rpt_start >= self.road_start_chainage:
            self.rpt_start = rpt_start

        self.rpt_end = self.road_end_chainage  # set to Road end chainage initially
        if rpt_end:
            if rpt_end > self.road_end_chainage:
                raise ValueError(
                    "Report End Chainage given is greater than Road's ending chainage"
                )
            elif rpt_end <= self.road_start_chainage:
                raise ValueError(
                    "Report End Chainage given is less than Road's starting chainage"
                )
            else:
                self.rpt_end = rpt_end

        self.build_sementations()

    def build_sementations(self):
        """ Create all of the segments based on report chainage start/end paramenters """
        self.segmentations = {
            item: {
                "chainage": float(item),
                "surf_cond": None,
                "date_surveyed": None,
                "survey_id": 0,
                "added_by": "",
            }
            for item in range(int(self.rpt_start), int(self.rpt_end))
        }

    def assign_survey_results(self):
        """ For all the Surveys, assign only the most up-to-date results to any given segment """
        for survey in self.surveys:
            # check survey does not overlap with current aggregate segmentations
            segment = self.segmentations[int(survey.chainage_start)]
            if (
                not segment["date_surveyed"]
                or survey.date_surveyed > segment["date_surveyed"]
            ):
                # TODO: Adjust Report start/end to ensure shorter than or equal to Survey start/end ??

                # update the segmentations & resolve overlapping survey segments
                for chainage in range(
                    int(survey.chainage_start), int(survey.chainage_end)
                ):
                    if (
                        not self.segmentations[chainage]["date_surveyed"]
                        or survey.date_surveyed
                        > self.segmentations[chainage]["date_surveyed"]
                    ):
                        self.segmentations[chainage]["surf_cond"] = survey.values[
                            "surface_condition"
                        ]
                        self.segmentations[chainage][
                            "date_surveyed"
                        ] = survey.date_surveyed
                        self.segmentations[chainage]["survey_id"] = survey.id
                        self.segmentations[chainage]["added_by"] = (
                            str(survey.user.id) if survey.user else ""
                        )

    def build_summary_stats(self):
        """ Generate the high-level counts & percentage statistics for the report """
        segments_length = len(self.segmentations)
        counts = Counter(
            [self.segmentations[segment]["surf_cond"] for segment in self.segmentations]
        )
        percentages = {
            condition: (counts[condition] / segments_length * 100)
            for condition in counts
        }
        setattr(self.report_protobuf, "counts", json.dumps(counts))
        setattr(self.report_protobuf, "percentages", json.dumps(percentages))

    def build_chainage_table(self):
        """ Generate the table of chainages the report """
        prev_cond, prev_date = None, None
        for segment in self.segmentations:
            segment = self.segmentations[segment]
            if (
                segment["surf_cond"] != prev_cond
                and segment["date_surveyed"] != prev_date
            ):
                entry = self.report_protobuf.table.add()
                setattr(entry, "chainage_start", segment["chainage"])
                setattr(entry, "surface_condition", str(segment["surf_cond"]))
                setattr(entry, "survey_id", segment["survey_id"])
                setattr(entry, "added_by", segment["added_by"])
                if segment["date_surveyed"]:
                    ts = Timestamp()
                    ts.FromDatetime(segment["date_surveyed"])
                    entry.date_surveyed.CopyFrom(ts)
                prev_cond, prev_date = (segment["surf_cond"], segment["date_surveyed"])

    def to_protobuf(self):
        """ Package up the various statistics and tables for export as Protobuf """
        self.report_protobuf = survey_pb2.Report()

        # set basic report attributes
        setattr(self.report_protobuf, "road_code", self.road_code)
        setattr(self.report_protobuf, "report_chainage_start", self.rpt_start)
        setattr(self.report_protobuf, "report_chainage_end", self.rpt_end)

        # build and set report statistical data & table
        self.assign_survey_results()
        self.build_summary_stats()
        self.build_chainage_table()

        return self.report_protobuf


def protobuf_surveys(request, chunk_name=None):
    """ returns a protobuf object with the set of all surveys or only of specific type"""

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    queryset = Survey.objects.all()
    if chunk_name:
        chunk_codes = Road.objects.filter(road_type=chunk_name).values("road_code")
        queryset = queryset.filter(road__in=chunk_codes)

    queryset.order_by("road", "chainage_start", "chainage_end", "-date_updated")
    surveys_protobuf = queryset.to_protobuf()

    return HttpResponse(
        surveys_protobuf.SerializeToString(), content_type="application/octet-stream"
    )


def protobuf_road_surveys(request, pk):
    """ returns a protobuf object with the set of surveys for a particular road pk"""

    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    # get the Road link requested
    road = get_object_or_404(Road.objects.all(), pk=pk)
    # pull any Surveys that cover some/all of the Road above
    queryset = (
        Survey.objects.filter(road=road.road_code)
        .filter(chainage_end__gte=road.link_start_chainage)
        .filter(chainage_start__lte=road.link_end_chainage)
    )
    queryset.order_by("road", "chainage_start", "chainage_end", "-date_updated")
    surveys_protobuf = queryset.to_protobuf()

    return HttpResponse(
        surveys_protobuf.SerializeToString(), content_type="application/octet-stream"
    )


def pbtimestamp_to_pydatetime(pb_stamp):
    """ Take a Protobuf Timestamp as single input and outputs a 
    time zone aware, Python Datetime object (UTC). Attempts to parse
    both with and without nanoseconds. """

    try:
        pb_date = datetime.strptime(pb_stamp.ToJsonString(), "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        pb_date = datetime.strptime(pb_stamp.ToJsonString(), "%Y-%m-%dT%H:%M:%S.%fZ")
    return pytz.utc.localize(pb_date)


def survey_create(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    if request.method != "POST":
        raise MethodNotAllowed(request.method)
    elif request.content_type != "application/octet-stream":
        return HttpResponse(status=400)

    # parse Survey from protobuf in request body
    req_pb = survey_pb2.Survey()
    req_pb.ParseFromString(request.body)

    # check that Protobuf parsed
    if not req_pb.road:
        return HttpResponse(status=400)

    try:
        with reversion.create_revision():
            survey = Survey.objects.create(
                **{
                    "road": req_pb.road,
                    "user": get_user_model().objects.get(pk=req_pb.user),
                    "chainage_start": req_pb.chainage_start,
                    "chainage_end": req_pb.chainage_end,
                    "date_surveyed": pbtimestamp_to_pydatetime(req_pb.date_surveyed),
                    "source": req_pb.source,
                    "values": json.loads(req_pb.values),
                }
            )

        # set new last_reversion_id on the protobuf to be returned
        versions = Version.objects.get_for_object(survey)
        req_pb.last_revision_id = versions[0].id

        response = HttpResponse(
            req_pb.SerializeToString(),
            status=200,
            content_type="application/octet-stream",
        )

        return response
    except Exception as err:
        return HttpResponse(status=400)


def survey_update(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    if request.method != "PUT":
        raise MethodNotAllowed(request.method)
    elif request.content_type != "application/octet-stream":
        return HttpResponse(status=400)

    # parse Survey from protobuf in request body
    req_pb = survey_pb2.Survey()
    req_pb.ParseFromString(request.body)

    # check that Protobuf parsed
    if not req_pb.id:
        return HttpResponse(status=400)

    # assert Survey ID given exists in the DB & there are changes to make
    survey = get_object_or_404(Survey.objects.filter(pk=req_pb.id))
    if Survey.objects.filter(pk=req_pb.id).to_protobuf().surveys[0] == req_pb:
        response = HttpResponse(
            req_pb.SerializeToString(),
            status=200,
            content_type="application/octet-stream",
        )
        return response

    # check if the survey has revision history, then check if survey
    # edits would be overwriting someone's changes
    version = Version.objects.get_for_object(survey).first()
    if version and req_pb.last_revision_id != version.revision.id:
        return HttpResponse(status=409)

    # update the Survey instance from PB fields
    try:
        survey.road = req_pb.road
        survey.user = get_user_model().objects.get(pk=req_pb.user)
        survey.chainage_start = req_pb.chainage_start
        survey.chainage_end = req_pb.chainage_end
        survey.date_surveyed = pbtimestamp_to_pydatetime(req_pb.date_surveyed)
        survey.source = req_pb.source
        survey.values = json.loads(req_pb.values)

        with reversion.create_revision():
            survey.save()
            # store the user who made the changes
            reversion.set_user(request.user)

        versions = Version.objects.get_for_object(survey)
        req_pb.last_revision_id = versions[0].id

        response = HttpResponse(
            req_pb.SerializeToString(),
            status=200,
            content_type="application/octet-stream",
        )
        return response
    except Exception as err:
        return HttpResponse(status=400)


def protobuf_road_audit(request, pk):
    """ returns a protobuf object with the set of all audit history items for a Road """

    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    queryset = Road.objects.all()
    road = get_object_or_404(queryset, pk=pk)
    versions = Version.objects.get_for_object(road)
    versions_protobuf = roads_pb2.Versions()

    for version in versions:
        version_pb = versions_protobuf.versions.add()
        setattr(version_pb, "pk", version.pk)
        setattr(version_pb, "user", _display_user(version.revision.user))
        setattr(version_pb, "comment", version.revision.comment)
        # set datetime field
        ts = Timestamp()
        ts.FromDatetime(version.revision.date_created)
        version_pb.date_created.CopyFrom(ts)
    return HttpResponse(
        versions_protobuf.SerializeToString(), content_type="application/octet-stream"
    )


def _display_user(user):
    """ returns the full username if populated, or the username, or "" """
    if not user:
        return ""
    user_display = user.get_full_name()
    return user_display or user.username
