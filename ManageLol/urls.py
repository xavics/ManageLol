from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'Manager.views.mainpage', name='main'),
    # url(r'^$', 'Manager.views.base', name='base'),
    url(r'^team/(\w+)/$', 'Manager.views.team', name='team'),
    url(r'^alert', 'Manager.views.alert', name='alert'),
    url(r'^reclamation', 'Manager.views.reclamation', name='reclamation'),
    url(r'^modify', 'Manager.views.modify', name='modify'),
    url(r'^game', 'Manager.views.game_ready', name='game'),
    url(r'^register','Manager.views.register', name='register'),
    url(r'^login','Manager.views.login_view', name='login'),
    url(r'^set_ip','Manager.views.set_ip', name='set_ip'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.BASE_DIR+'/TwitApp'+settings.MEDIA_URL}),
    url(r'^logout', 'Manager.views.user_logout', name='logout'),
    # url(r'^logout', 'django.contrib.auth.views.logout', { 'next_page': '/'}),
    url(r'^a_ref', 'Manager.views.auth_ref', name='auth_ref'),
    url(r'^referee', 'Manager.views.referee', name='referee'),
    url(r'^resolve/(\w+)/$', 'Manager.views.resolve_reclamation', name='resolve_reclamation'),
    url(r'^close_registers', 'Manager.views.close_registers', name='close_registers'),
)
