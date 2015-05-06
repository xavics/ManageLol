from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'Manager.views.mainpage', name='main'),
    url(r'^register','Manager.views.register', name='register'),
    url(r'^login','Manager.views.login_view', name='login'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.BASE_DIR+'/TwitApp'+settings.MEDIA_URL}),

)
