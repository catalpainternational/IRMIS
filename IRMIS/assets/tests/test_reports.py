from datetime import datetime

from django.urls import reverse
from django.utils.timezone import make_aware

from rest_framework.exceptions import MethodNotAllowed, ValidationError
from protobuf import report_pb2

import json
import pytest

from ..models import Road, Survey


@pytest.mark.django_db
def test_report_protobuf_requires_auth(client):
    """ This test will fail if an unauthenticated request can access the reports api """
    url = reverse("protobuf_reports")
    response = client.get(url)
    assert response.status_code == 302


def create_user(client, django_user_model):
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    return user


@pytest.mark.django_db
def test_report_protobuf_get_only(client, django_user_model):
    """ This test will fail if any non-GET request can access the reports api """
    user = create_user(client, django_user_model)

    # hit the reports api with POST, PATCH, PUT, DELETE expecting a MethodNotAllowed raise
    url = reverse("protobuf_reports")
    with pytest.raises(MethodNotAllowed):
        response = client.post(url)

    with pytest.raises(MethodNotAllowed):
        response = client.patch(url)

    with pytest.raises(MethodNotAllowed):
        response = client.put(url)

    with pytest.raises(MethodNotAllowed):
        response = client.delete(url)


@pytest.mark.django_db
def test_report_protobuf_filter_check(client, django_user_model):
    """ This test will fail if a request to the reports API does not meet the requirements for filters """
    user = create_user(client, django_user_model)

    # hit the reports api with POST, PATCH, PUT, DELETE
    url = reverse("protobuf_reports")
    response = client.get(url)
    assert response.status_code == 400


@pytest.mark.django_db
def test_report_protobuf_simple(client, django_user_model):
    """ This test will succeed with a simple request """
    user = create_user(client, django_user_model)

    # hit the reports api with a primaryattribute
    url = reverse("protobuf_reports")
    response = client.get(
        url,
        {
            "reportassettype": ["BRDG", "CULV", "DRFT"],
            "primaryattribute": ["asset_condition"],
        },
    )
    assert response.status_code == 200

    # parse report from protobuf in response content
    rsp_pb = report_pb2.Report()
    rsp_pb.ParseFromString(response.content)
    assert rsp_pb.filter

    filter = json.loads(rsp_pb.filter)
    lengths = json.loads(rsp_pb.lengths)
    assert filter["primary_attribute"] == ["asset_condition"]
    assert filter["asset_type"] == ["BRDG", "CULV", "DRFT"]


def create_base_survey_dict_from_road(road):
    return {
        "asset_id": "ROAD{}".format(road.pk),
        "asset_code": road.road_code,
        "date_surveyed": make_aware(datetime(1970, 1, 1)),
        "user_id": None,
        "chainage_start": road.geom_start_chainage,
        "chainage_end": road.geom_end_chainage,
        "values": {"asset_class": "NAT", "asset_condition": None},
    }


@pytest.mark.django_db
def test_report_protobuf_standard(client, django_user_model):
    """ This test will succeed with a normal request for a single attribute for a single asset """
    user = create_user(client, django_user_model)

    # create a whole series of surveys that test a variety of conditions that the report query must handle
    # define roads
    r0 = {
        "road_code": "A01",
        "link_code": "A01-01",
        "asset_class": "NAT",
        "asset_condition": None,
        "link_start_chainage": 0,
        "link_end_chainage": 62405,
        "geom_start_chainage": 0,
        "geom_end_chainage": 62405,
    }
    r1 = {
        "road_code": "A01",
        "link_code": "A01-02",
        "asset_class": "NAT",
        "asset_condition": None,
        "link_start_chainage": 62405,
        "link_end_chainage": 121841,
        "geom_start_chainage": 62405,
        "geom_end_chainage": 121841,
    }
    r2 = {
        "road_code": "A01",
        "link_code": "A01-03",
        "asset_class": "NAT",
        "asset_condition": None,
        "link_start_chainage": 121841,
        "link_end_chainage": 181425,
        "geom_start_chainage": 121841,
        "geom_end_chainage": 181425,
    }
    r3 = {
        "road_code": "A01",
        "link_code": "A01-04",
        "asset_class": "NAT",
        "asset_condition": None,
        "link_start_chainage": 181425,
        "link_end_chainage": 202312,
        "geom_start_chainage": 181425,
        "geom_end_chainage": 202312,
    }
    rr0 = Road.objects.create(**r0)
    rr1 = Road.objects.create(**r1)
    rr2 = Road.objects.create(**r2)
    rr3 = Road.objects.create(**r3)

    # define base surveys
    b0 = create_base_survey_dict_from_road(rr0)
    b1 = create_base_survey_dict_from_road(rr1)
    b2 = create_base_survey_dict_from_road(rr2)
    b3 = create_base_survey_dict_from_road(rr3)
    # define user surveys
    u0 = {
        "asset_id": "ROAD{}".format(rr0.pk),
        "asset_code": rr0.road_code,
        "date_surveyed": make_aware(datetime(2020, 5, 25)),
        "user_id": user.pk,
        "chainage_start": 18000,
        "chainage_end": 18100,
        "values": {"asset_condition": 4},
    }
    u1 = {
        "asset_id": "ROAD{}".format(rr0.pk),
        "asset_code": rr0.road_code,
        "date_surveyed": make_aware(datetime(2020, 5, 26)),
        "user_id": user.pk,
        "chainage_start": 19000,
        "chainage_end": 19050,
        "values": {"asset_condition": 3},
    }
    u2 = {
        "asset_id": "ROAD{}".format(rr0.pk),
        "asset_code": rr0.road_code,
        "date_surveyed": make_aware(datetime(2020, 5, 27)),
        "user_id": user.pk,
        "chainage_start": 18050,
        "chainage_end": 18125,
        "values": {"asset_condition": 2},
    }
    u3 = {
        "asset_id": "ROAD{}".format(rr0.pk),
        "asset_code": rr0.road_code,
        "date_surveyed": make_aware(datetime(2020, 6, 2)),
        "user_id": user.pk,
        "chainage_start": rr0.geom_start_chainage,
        "chainage_end": 1000,
        "values": {"asset_condition": 1},
    }
    u4 = {
        "asset_id": "ROAD{}".format(rr1.pk),
        "asset_code": rr1.road_code,
        "date_surveyed": make_aware(datetime(2020, 6, 2)),
        "user_id": user.pk,
        "chainage_start": 65000,
        "chainage_end": 66000,
        "values": {"asset_condition": 4},
    }

    sb0 = Survey.objects.create(**b0)
    sb1 = Survey.objects.create(**b1)
    sb2 = Survey.objects.create(**b2)
    sb3 = Survey.objects.create(**b3)

    su0 = Survey.objects.create(**u0)
    su1 = Survey.objects.create(**u1)
    su2 = Survey.objects.create(**u2)
    su3 = Survey.objects.create(**u3)
    su4 = Survey.objects.create(**u4)

    # hit the reports api with a primaryattribute
    url = reverse("protobuf_reports")
    response = client.get(
        url,
        {
            "reportassettype": ["ROAD"],
            "primaryattribute": ["asset_condition"],
            "asset_code": ["A01"],
            "chainageend": 62405,
        },
    )
    assert response.status_code == 200

    # parse report from protobuf in response content
    rsp_pb = report_pb2.Report()
    rsp_pb.ParseFromString(response.content)
    assert rsp_pb.filter
    # once the test setup is correct this will have the results in it
    assert rsp_pb.lengths == "{}"

    filter = json.loads(rsp_pb.filter)
    lengths = json.loads(rsp_pb.lengths)
    assert filter["primary_attribute"] == ["asset_condition"]
    assert filter["asset_type"] == ["ROAD"]
    assert filter["asset_code"] == ["A01"]
