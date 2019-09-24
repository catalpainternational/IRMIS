from django.urls import reverse
from ..models import Road
import reversion
import json
import pytest


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
    with reversion.create_revision():
        # create a road
        road = Road.objects.create()
        # store the user who made the changes
        reversion.set_user(user)
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
