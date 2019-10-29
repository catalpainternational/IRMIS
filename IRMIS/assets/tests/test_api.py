from django.urls import reverse
from django.utils import timezone
from ..models import Road, Survey
from protobuf import roads_pb2, survey_pb2
from reversion.models import Version
from google.protobuf.timestamp_pb2 import Timestamp

import reversion
import pytest
import json
import time


@pytest.mark.django_db
def test_api_requires_auth(client):
    """ This test will fail if an unauthenticated request can access the roads api """
    # LIST roads endpoint
    url = reverse("road-list")
    response = client.get(url)
    assert response.status_code == 403
    # RETRIEVE single road endpoint
    road = Road.objects.create()
    url = reverse("road-detail", kwargs={"pk": road.pk})
    response = client.get(url)
    assert response.status_code == 403
    # UPDATE single road endpoint
    url = reverse("road_update")
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_road_api_list_does_not_error(client, django_user_model):
    """ This test will fail if the road list api throws an error """
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    # hit the road api
    url = reverse("road-list")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_road_api_detail_does_not_error(client, django_user_model):
    """ This test will fail if the road list api throws an error """
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    with reversion.create_revision():
        # create a road
        road = Road.objects.create()
        # store the user who made the changes
        reversion.set_user(user)
    # hit the road api - detail
    url = reverse("road-detail", kwargs={"pk": road.pk})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_road_api_all_but_GET_PUT_should_fail(client, django_user_model):
    """ This test will fail if the road api allows POST, PATCH, or DELETE methods
    through (non 405 status)"""
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    # create an empty pb for testing the endpoints
    pb = roads_pb2.Road()
    pb_str = pb.SerializeToString()
    # hit the road api - detail endpoints
    url = reverse("road-detail", kwargs={"pk": pb.id})
    response = client.post(url, data=pb_str, content_type="application/octet-stream")
    assert response.status_code == 405
    response = client.patch(url, data=pb_str, content_type="application/octet-stream")
    assert response.status_code == 405
    response = client.delete(url, data=pb_str, content_type="application/octet-stream")
    assert response.status_code == 405


@pytest.mark.django_db
def test_road_edit_update(client, django_user_model):
    """ This test will fail if the road api throws an error with update of
    road asset or fails to change the road_name field """
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    with reversion.create_revision():
        # create a road
        road = Road.objects.create()
        # store the user who made the changes
        reversion.set_user(user)
    # build protobuf to send with road modifications
    pb = Road.objects.filter(id=road.id).to_protobuf().roads[0]
    pb.road_name = "Pizza The Hutt"
    # hit the road api - detail
    url = reverse("road_update")
    response = client.put(
        url, data=pb.SerializeToString(), content_type="application/octet-stream"
    )
    assert response.status_code == 200
    # check that DB was updated correctly
    mod_road = Road.objects.get(id=road.id)
    assert mod_road.road_name == pb.road_name
    # check that a new revision exists
    versions = Version.objects.get_for_object(mod_road)
    assert len(versions) == 2
    # check that the user is noted in the latest revision record
    assert versions[1].revision.user == user


@pytest.mark.django_db
def test_road_edit_update_bad_fk_code(client, django_user_model):
    """ This test will fail if the road api does NOT throw an error when attempting
    to update a road asset when passed a bad FK code """
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    with reversion.create_revision():
        # create a road
        road = Road.objects.create()
        # store the user who made the changes
        reversion.set_user(user)
    # build protobuf to send with road modifications
    pb = Road.objects.filter(id=road.id).to_protobuf().roads[0]
    pb.road_status = "2"
    # hit the road api - detail
    url = reverse("road_update")
    response = client.put(
        url, data=pb.SerializeToString(), content_type="application/octet-stream"
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_road_edit_update_404_pk(client, django_user_model):
    """ This test will fail if the road api does NOT throw a 404 error when attempting
    to update a road asset when passed Road ID does not exist in the DB """
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    # build protobuf to send with road modifications
    pb = roads_pb2.Road()
    pb.id = 99999
    # hit the road api - detail
    url = reverse("road_update")
    response = client.put(
        url, data=pb.SerializeToString(), content_type="application/octet-stream"
    )
    assert response.status_code == 404


@pytest.mark.django_db
def test_road_edit_erroneous_protobuf(client, django_user_model):
    """ This test will fail if the road api does NOT throw an error when given
    a protobuf payload that is 1) not deserializable or 2) doesn't point to an
    existing Road in the DB (CREATE attempt, not proper PUT) """
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    url = reverse("road_update")
    response = client.put(url, data=b"", content_type="application/octet-stream")
    assert response.status_code == 400


@pytest.mark.django_db
def test_road_edit_identical_data(client, django_user_model):
    """ This test will fail if the road api does not throw a 200 response when
    passed data identical to that which already exists on server. Header should contain
    'Location' to point to the updated data."""
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    with reversion.create_revision():
        # create a road
        road = Road.objects.create()
        # store the user who made the changes
        reversion.set_user(user)
    # make Protobuf identical to existing Road
    pb = Road.objects.filter(id=road.id).to_protobuf().roads[0]
    pb_str = pb.SerializeToString()
    # hit the road api - detail
    url = reverse("road_update")
    response = client.put(url, data=pb_str, content_type="application/octet-stream")
    assert response.status_code == 200


@pytest.mark.django_db
def test_road_edit_detect_another_users_previous_changes(client, django_user_model):
    """ This test will fail if the road api does not throw a 409 response when
    passed which has been updated/edited by another user since the client recieved thier
    data from the server. Header should contain 'Location' to point to the updated data."""
    # create two users
    user1 = django_user_model.objects.create_user(username="user1", password="bar")
    user2 = django_user_model.objects.create_user(username="user2", password="bar")
    # login with user1
    client.force_login(user1)
    with reversion.create_revision():
        # create a road
        road = Road.objects.create()
        # store the user who made the changes
        reversion.set_user(user1)
    # make Protobuf identical to existing Road, but change one detail
    pb = Road.objects.filter(id=road.id).to_protobuf().roads[0]
    pb.road_name = "Pizza the Hutt Rd"
    pb_str = pb.SerializeToString()
    time.sleep(1)
    # User2 updates Road on the server
    with reversion.create_revision():
        road.road_name = "Sir Anders Blvd"
        road.save()
        # store the user who made the changes
        reversion.set_user(user2)
    # hit the road api - detail
    url = reverse("road_update")
    response = client.put(url, data=pb_str, content_type="application/octet-stream")
    assert response.status_code == 409


@pytest.mark.django_db
def test_api_lastmod_and_etag_present(client, django_user_model):
    """ check the road api etag and last-modified are present on requests """
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    # create a road
    road = Road.objects.create()
    # hit the road api
    url = reverse("road-detail", kwargs={"pk": road.pk})
    response = client.get(url)
    # check the response has both etag & last-modified attributes
    assert response["etag"] and response["last-modified"]


@pytest.mark.django_db
def test_api_etag_caches(client, django_user_model):
    """ check the road api etag integration """
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    # create a road
    road = Road.objects.create()
    # hit the road api
    url = reverse("road-detail", kwargs={"pk": road.pk})
    response = client.get(url)
    # get the etag value from the response
    etag = response["etag"]
    # send another response with the etag set
    response2 = client.get(url, HTTP_IF_NONE_MATCH=etag)
    # check the response2 is 304
    assert response2.status_code == 304


@pytest.mark.django_db
def test_survey_create(client, django_user_model):
    """ This test will fail if the survey api throws an error with creating
    a survey asset """
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    # build protobuf to send new survey
    pb = survey_pb2.Survey()
    pb.user = user.pk
    pb.road = "A01"
    pb.chainage_start = 6000.0
    pb.chainage_end = 7000.0
    pb.values = json.dumps({"traffic_level": "None", "surface_condition": "2"})
    ts = Timestamp()
    ts.FromDatetime(timezone.now())
    pb.date_surveyed.CopyFrom(ts)
    # hit the survey API
    url = reverse("survey_create")
    response = client.post(
        url, data=pb.SerializeToString(), content_type="application/octet-stream"
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_survey_edit_update(client, django_user_model):
    """ This test will fail if the survey api throws an error with update of
    survey asset or fails to change the chainage start field """
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    with reversion.create_revision():
        # create a survey
        survey = Survey.objects.create(
            **{
                "road": "A01",
                "user": user,
                "chainage_start": 600.0,
                "chainage_end": 700.25,
                "date_surveyed": timezone.now(),
                "values": {"surface_condition": "2", "traffic_level": "L"},
            }
        )
        # store the user who made the changes
        reversion.set_user(user)
    # build protobuf to send with road modifications
    pb = Survey.objects.filter(id=survey.id).to_protobuf().surveys[0]
    pb.chainage_start = 500.0
    # hit the survey api
    url = reverse("survey_update")
    response = client.put(
        url, data=pb.SerializeToString(), content_type="application/octet-stream"
    )
    assert response.status_code == 200
    # check that DB was updated correctly
    mod_survey = Survey.objects.get(id=survey.id)
    assert mod_survey.chainage_start == pb.chainage_start
    # check that a new revision exists
    versions = Version.objects.get_for_object(mod_survey)
    assert len(versions) == 2
    # check that the user is noted in the latest revision record
    assert versions[1].revision.user == user


@pytest.mark.django_db
def test_survey_edit_update_404_pk(client, django_user_model):
    """ This test will fail if the survey api does NOT throw a 404 error when attempting
    to update a road asset when passed Road ID does not exist in the DB """
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    # build protobuf to send with survey modifications
    pb = survey_pb2.Survey()
    pb.id = 99999
    # hit the survey api - detail
    url = reverse("survey_update")
    response = client.put(
        url, data=pb.SerializeToString(), content_type="application/octet-stream"
    )
    assert response.status_code == 404


@pytest.mark.django_db
def test_survey_edit_erroneous_protobuf(client, django_user_model):
    """ This test will fail if the survey api does NOT throw an error when given
    a protobuf payload that is 1) not deserializable or 2) doesn't point to an
    existing Survey in the DB (CREATE attempt, not proper PUT) """
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    url = reverse("survey_update")
    response = client.put(url, data=b"", content_type="application/octet-stream")
    assert response.status_code == 400


@pytest.mark.django_db
def test_survey_delete(client, django_user_model):
    """ This test will fail if the survey api throws an error with deletion of
    survey asset """
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    with reversion.create_revision():
        # create a survey
        survey = Survey.objects.create(
            **{
                "road": "A01",
                "user": user,
                "chainage_start": 600.0,
                "chainage_end": 700.25,
                "date_surveyed": timezone.now(),
                "values": {"surface_condition": "2", "traffic_level": "L"},
            }
        )
        # store the user who made the changes
        reversion.set_user(user)

    # attempt to delete the survey
    url = reverse("survey_delete", kwargs={"pk": str(survey.id)})
    response = client.get(url)

    assert response.status_code == 200
    # check that DB not longer has the survey
    mod_survey = Survey.objects.filter(id=survey.id).all()
    assert len(mod_survey) == 0


@pytest.mark.django_db
def test_survey_delete_404_pk(client, django_user_model):
    """ This test will fail if the survey api does NOT throw a 404 error when attempting
    to delete a survey with an ID that does not exist in the DB """
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)

    # hit the survey api
    url = reverse("survey_delete", kwargs={"pk": 999999})
    response = client.get(url)
    assert response.status_code == 404
