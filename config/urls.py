from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from core.sitemaps import StaticSitemap
from core.views import robots_txt

admin.site.site_header = "Bhumi Pathways: Site Administration"
admin.site.site_title = "Bhumi Pathways Admin"
admin.site.index_title = "Edit website content and manage enquiries"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": {"pages": StaticSitemap}}, name="sitemap"),
    path("robots.txt", robots_txt, name="robots"),
    path("", include("core.urls")),
]
