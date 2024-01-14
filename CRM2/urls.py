from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from website.views import landing_page, LandingPageView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='landing-page'),
    path("website/", include("website.urls", namespace="website")),
]


if settings.DEBUG is True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)