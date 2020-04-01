from . import auto_viewsets
from rest_framework import routers


def router_factory():
    router = routers.DefaultRouter()
    for vs in auto_viewsets.generated:
        router.register(
            prefix=vs.serializer_class.Meta.model._meta.model_name,
            viewset=vs,
            basename="auto-api-%s" % (vs.serializer_class.Meta.model._meta.model_name,),
        )
    router.register(
        prefix="project_extended",
        viewset=auto_viewsets.ProjectViewset,
        basename="auto-api-%s" % ("project_extended",),
    )
    return router
