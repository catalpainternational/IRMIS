from django.test import TestCase
from django.urls import reverse
from .models import Road
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
    # create a road
    road = Road.objects.create()
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    # hit the road api
    url = reverse("road-list")
    response = client.get(url)


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
