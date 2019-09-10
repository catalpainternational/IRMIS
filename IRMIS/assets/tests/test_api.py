from django.urls import reverse
from ..models import Road
from protobuf import roads_pb2
from reversion.models import Version
import reversion
import pytest
import json


@pytest.mark.django_db
def test_api_requires_auth(client):
    """ This test will fail if an unauthenticated request can access the roads api """
    url = reverse("road-list")
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
    # create a road
    road = Road.objects.create()
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
    # create a road for testing the endpoints
    road = Road.objects.create()
    # hit the road api - detail endpoints
    url = reverse("road-detail", kwargs={"pk": road.pk})
    response = client.post(url, data=json.dumps({}), content_type="application/json")
    assert response.status_code == 405
    response = client.patch(url, data=json.dumps({}), content_type="application/json")
    assert response.status_code == 405
    response = client.delete(url, data=json.dumps({}), content_type="application/json")
    assert response.status_code == 405


@pytest.mark.django_db
def test_road_edit_update(client, django_user_model):
    """ This test will fail if the road api throws an error with update of
    road asset or fails to change the road_name field """
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    # create a road
    with reversion.create_revision():
        road = Road.objects.create()
    # build protobuf to send with road modifications
    pb = roads_pb2.Road()
    pb.id = road.id
    pb.road_name = "Pizza The Hutt"
    # hit the road api - detail
    url = reverse("road_update")
    response = client.put(
        url, data=pb.SerializeToString(), content_type="application/octet-stream"
    )
    assert response.status_code == 204
    # check that DB was updated correctly
    mod_road = Road.objects.get(id=road.id)
    assert mod_road.road_name == pb.road_name
    # check that a reversion exists
    versions = Version.objects.get_for_object(mod_road)
    assert len(versions) == 2


@pytest.mark.django_db
def test_road_edit_update_bad_fk_code(client, django_user_model):
    """ This test will fail if the road api does NOT throw an error when attempting
    to update a road asset when passed a bad FK code """
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    # create a road
    road = Road.objects.create()
    # build protobuf to send with road modifications
    pb = roads_pb2.Road()
    pb.id = road.id
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
    to update a road asset when passed PK code does not exist in the DB """
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    # create a road
    road = Road.objects.create()
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
    # create a road
    road = Road.objects.create()
    # build protobuf to send with road modifications
    pb = roads_pb2.Road()
    pb.id = road.id
    pb.road_name = "Pizza The Hutt"
    # try to pass a bad Protobuf string
    pb_string = pb.SerializeToString()
    bad_pb_string = b""
    url = reverse("road_update")
    response = client.put(
        url, data=bad_pb_string, content_type="application/octet-stream"
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_road_edit_identical_data(client, django_user_model):
    """ This test will fail if the road api does not throw a 204 response when
    passed data identical to that which already exists on server. Header should contain
    'Location' to point to the updated data."""
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    # create a road & protobuf to send
    road = Road.objects.create()
    # make Protobuf identical to existing Road
    pb = Road.objects.filter(id=road.id).to_protobuf().roads[0]
    # hit the road api - detail
    url = reverse("road_update")
    response = client.put(
        url, data=pb.SerializeToString(), content_type="application/octet-stream"
    )
    assert response.status_code == 204


@pytest.mark.django_db
def test_api_lastmod_and_etag_present(client, django_user_model):
    """ check the road api etag and last-modified are present on requests """

    # create a road
    road = Road.objects.create()
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    # hit the road api
    url = reverse("road-detail", kwargs={"pk": road.pk})
    response = client.get(url)
    # check the response has both etag & last-modified attributes
    assert response["etag"] and response["last-modified"]


@pytest.mark.django_db
def test_api_etag_caches(client, django_user_model):
    """ check the road api etag integration """

    # create a road
    road = Road.objects.create()
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    # hit the road api
    url = reverse("road-detail", kwargs={"pk": road.pk})
    response = client.get(url)
    # get the etag value from the response
    etag = response["etag"]
    # send another response with the etag set
    response2 = client.get(url, HTTP_IF_NONE_MATCH=etag)
    # check the response2 is 304
    assert response2.status_code == 304
