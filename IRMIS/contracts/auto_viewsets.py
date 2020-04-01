from rest_framework.viewsets import ModelViewSet
from . import auto_serializers
from . import models

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


generated = [
    type(
        "%sViewSet" % (ser.Meta.model._meta.object_name,),
        (ModelViewSet,),
        dict(
            serializer_class=ser,
            queryset=ser.Meta.model.objects.all(),
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[IsAuthenticated],
        ),
    )
    for ser in auto_serializers.generated
]


class ProjectViewset(ModelViewSet):
    """
    A comprehensive ViewSet for editing Projects and accessing related Milestones and Budgets.
    """

    queryset = models.Project.objects.all()
    serializer_class = auto_serializers.ProjectSerializer
    permission_classes = [IsAuthenticated]
