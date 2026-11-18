from django.contrib import admin
from django.urls import path, include

from core.seo import robots_txt, sitemap_xml

urlpatterns = [
    path('admin/', admin.site.urls),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap_xml, name='sitemap_xml'),
    path('', include('core.urls', namespace='core')),
]