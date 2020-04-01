from . import models
from rest_framework.serializers import ModelSerializer
from django.db.models.base import ModelBase

generated = [
    type(
        "%sSerializer" % model_name,
        (ModelSerializer,),
        {"Meta": type("Meta", (type,), dict(model=model, fields="__all__"))},
    )
    for model_name, model in vars(models).items()
    if isinstance(model, ModelBase) and not model._meta.abstract
]


class ProjectBudgetSerializer(ModelSerializer):
    class Meta:
        model = models.ProjectBudget
        fields = [
            "project",
            "id",
            "start_date",
            "end_date",
            "approved_value",
        ]


class ProjectMilestoneSerializer(ModelSerializer):
    class Meta:
        model = models.ProjectMilestone
        fields = ["project", "id", "date", "progress"]


class ProjectAssetSerializer(ModelSerializer):
    class Meta:
        model = models.ProjectAsset
        fields = ["project", "id", "asset_end_chainage", "asset_end_chainage"]


class ProjectSerializer(ModelSerializer):

    budgets = ProjectBudgetSerializer(many=True, read_only=True)
    milestones = ProjectMilestoneSerializer(many=True, read_only=True)
    assets = ProjectAssetSerializer(many=True, read_only=True)

    class Meta:
        model = models.Project
        fields = [
            "status",
            "program",
            "type_of_work",
            "name",
            "code",
            "description",
            "funding_source",
            "donor",
            "construction_period_start",
            "construction_period_end",
            # M2M fields
            "milestones",
            "budgets",
            "assets",
        ]
