"""IRMIS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.gis import admin
from django.contrib.auth import urls as django_auth_urls
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls import i18n as i18n_urls
from django.conf.urls.static import static
from django.urls import path, re_path, include, reverse_lazy

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls


def trigger_error(request):
    division_by_zero = 1 / 0  # noqa


urlpatterns = [
    path("assets/", include("assets.urls")),
    path("admin/", admin.site.urls),
    path("sentry-debug/", trigger_error),
    re_path(r"^cms/", include(wagtailadmin_urls)),
    re_path(r"^documents/", include(wagtaildocs_urls)),
    re_path(
        r"^accounts/password_reset/$",
        auth_views.PasswordResetView.as_view(
            html_email_template_name="registration/password_reset_email.html"
        ),
    ),
    re_path(r"^accounts/", include(django_auth_urls)),
    re_path(r"^i18n/", include(i18n_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += [re_path(r"^rosetta/", include("rosetta.urls"))]

# catchall must come last
urlpatterns += [re_path(r"", include(wagtail_urls))]
