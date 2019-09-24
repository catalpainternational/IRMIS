from django.urls import reverse
from ..models import Road
import reversion
import pytest


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
    with reversion.create_revision():
        # create a road
        road = Road.objects.create()
        # store the user who made the changes
        reversion.set_user(user)
    # hit the road api
    url = reverse("protobuf_roads")
    response = client.get(url)
    assert response.status_code == 200
