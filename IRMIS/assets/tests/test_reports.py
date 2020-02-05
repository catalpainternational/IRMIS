from django.urls import reverse
from rest_framework.exceptions import MethodNotAllowed, ValidationError
from protobuf import report_pb2
import json
import pytest


@pytest.mark.django_db
def test_report_protobuf_requires_auth(client):
    """ This test will fail if an unauthenticated request can access the reports api """
    url = reverse("protobuf_reports")
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_report_protobuf_get_only(client, django_user_model):
    """ This test will fail if any non-GET request can access the reports api """
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)

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
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)

    # hit the reports api with POST, PATCH, PUT, DELETE
    url = reverse("protobuf_reports")
    with pytest.raises(ValidationError):
        response = client.get(url)


@pytest.mark.django_db
def test_report_protobuf_simple(client, django_user_model):
    """ This test will succeed with a simple request """
    # create a user
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)

    # hit the reports api with a primaryattribute
    url = reverse("protobuf_reports")
    response = client.get(url, {"primaryattribute": ["asset_condition"]})
    assert response.status_code == 200

    # parse report from protobuf in response content
    rsp_pb = report_pb2.Report()
    rsp_pb.ParseFromString(response.content)
    assert rsp_pb.filter

    filter = json.loads(rsp_pb.filter)
    lengths = json.loads(rsp_pb.lengths)
    assert filter["primary_attribute"] == ["asset_condition"]
