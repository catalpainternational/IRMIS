from django.urls import reverse
import pytest


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
    # hit the road api
    url = reverse("geojson_details")
    response = client.get(url)
    assert response.status_code == 200
