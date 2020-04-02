from django.test import TestCase
import pytest
from django.urls import reverse
import json
from .. import models

# Create your tests here.


class TestData:
    @staticmethod
    def project():
        return {
            "status": models.ProjectStatus.objects.get_or_create(name="Planning")[0].pk,
            "program": models.Program.objects.get_or_create(
                name="Programa de estradas"
            )[0].pk,
            "type_of_work": models.TypeOfWork.objects.get_or_create(
                name="Routine maintenance"
            )[0].pk,
            "name": "Hello WOrld",
            "code": "1243",
            "description": "1243",
            "asset_code": "1324",
            "funding_source": models.FundingSource.objects.get_or_create(
                name="Unknown"
            )[0].pk,
            "construction_period_start": "2020-02-05",
            "construction_period_end": "2020-02-05",
        }

    milestone = {"days_of_work": 10, "progress": 20}

    budget = {
        "start_date": "2020-02-05",
        "end_date": "2020-02-15",
        "approved_value": "901.0000",
    }


@pytest.mark.django_db
def test_contracts_api_requires_auth(client):
    """ This test will fail if an unauthenticated request can access the contracts api """
    url = reverse("auto-api-project_extended-list")
    response = client.get(url)
    assert response.status_code in [401, 403]


@pytest.mark.django_db
def test_contracts_api(client, django_user_model):
    """ This test will pass if an authenticated request can access the contracts api """
    url = reverse("auto-api-project_extended-list")
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_contracts_PUT_project(client, django_user_model):
    """ This test will PUT a project """
    url = reverse("auto-api-project-list")
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    response = client.post(
        url, data=TestData.project(), content_type="application/json",
    )
    assert response.status_code == 201


@pytest.mark.django_db
def test_contracts_PUT_budget(client, django_user_model):
    """ This test will PUT a project """
    url = reverse("auto-api-project-list")
    user = django_user_model.objects.create_user(username="user1", password="bar")
    client.force_login(user)
    response = client.post(
        url, data=TestData.project(), content_type="application/json",
    )

    assert response.status_code == 201

    # Use this project id to create Milestone and Budget
    project_id = response.json()["id"]

    # PUT a milestone for this project
    url = reverse("auto-api-projectmilestone-list")

    response = client.post(
        url,
        data={**TestData.milestone, "project": project_id},
        content_type="application/json",
    )

    assert response.status_code == 201

    # PUT a budget for this project
    url = reverse("auto-api-projectbudget-list")

    response = client.post(
        url,
        data={**TestData.budget, "project": project_id},
        content_type="application/json",
    )

    assert response.status_code == 201
