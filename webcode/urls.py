from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webcode.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/', 'webpy.views.index'),
    url(r'^submit/', 'webpy.views.submit'),
    url(r'^run/', 'webpy.views.run'),
    url(r'^debug/', 'webpy.views.debug'),
    url(r'^gdb/', 'webpy.views.gdb'),
    url(r'^console/', 'webpy.views.tty'),
    url(r'^websocks/', 'webpy.views.websocks'),


) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
