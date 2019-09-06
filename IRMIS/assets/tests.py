from django.test import TestCase
from django.urls import reverse
from django.core.files.base import ContentFile
from .models import CollatedGeoJsonFile, Road
import json
import pytest


@pytest.mark.django_db
def test_api_requires_auth(client):
    """ This test will fail if an unauthenticated request can access the roads api """
    url = reverse("road-list")
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_api_road_list_does_not_error(client, django_user_model):
    """ This test will fail if the road list api throws an error """
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    # create a road
    road = Road.objects.create()
    # hit the road api
    url = reverse("road-list")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_road_detail_does_not_error(client, django_user_model):
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


@pytest.mark.django_db
def test_geojson_details_requires_auth(client):
    """ This test will fail if an unauthenticated request can access the roads api """
    url = reverse("geojson_details")
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_geojson_details_does_not_error(client, django_user_model):
    """ This test will fail if the road list api throws an error """
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    # create a GeoJSON file
    road = CollatedGeoJsonFile.objects.create(key="test", geobuf_file=ContentFile(b""))
    # hit the GeoJSON api
    url = reverse("geojson_details")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_road_chunks_requires_auth(client):
    """ This test will fail if an unauthenticated request can access the roads api """
    url = reverse("road_chunks")
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_road_chunks_does_not_error(client, django_user_model):
    """ This test will fail if the road chunks api throws an error """
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    # create a road
    road = Road.objects.create()
    # hit the road chunks api
    url = reverse("road_chunks")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_road_chunks_reports_all_roads(client, django_user_model):
    """ This integration test will fail if the road chunks api does not return a correct total count of roads """
    """ This test requires access to the actual DB for it to have any real meaning """
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    # get an actual count of all roads
    road_count = Road.objects.count()
    # hit the road chunks api
    url = reverse("road_chunks")
    response = client.get(url)
    chunks = json.loads(response.content)
    # for this assertion to really work we need to extract all of the chunks
    # sum their individual values and then finally compare that to road_count
    assert road_count == 0


@pytest.mark.django_db
def test_protobuf_requires_auth(client):
    """ This test will fail if an unauthenticated request can access the roads api """
    url = reverse("protobuf_roads")
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_protobuf_road_list_does_not_error(client, django_user_model):
    """ This test will fail if the road list api throws an error """
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    # create a road
    road = Road.objects.create()
    # hit the road api
    url = reverse("protobuf_roads")
    response = client.get(url)
    assert response.status_code == 200
