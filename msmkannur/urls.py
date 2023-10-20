from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.generic import TemplateView


urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("main/", include("main.urls", namespace="main")),
        path("", include("highsec.urls", namespace="highsec")),
        path("sitemap.xml", TemplateView.as_view(template_name="sitemap.xml", content_type="text/xml")),
        path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

admin.site.site_header = "MSM Kannur Administration"
admin.site.site_title = "MSM Kannur Admin Portal"
admin.site.index_title = "Welcome to MSM Kannur Admin Portal"
