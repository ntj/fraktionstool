from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from fraktionstool.views import NachrichtenList
from fraktionstool.views import list_gremien, list_vorhaben, list_nachrichten

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', login_required(NachrichtenList.as_view()), name='ftool-home'),
    url(r'^nachrichten/gremium/(?P<gremium>-?\d+)/showall/(?P<show_all>[01])/vorhaben/(?P<vorhaben>-?\d+)/$',
        login_required(NachrichtenList.as_view()), name='ftool-home-gremium'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', {'template_name': 'login.html'},
        name='mysite_login'),
    url(r'^logout/$', 'logout', {'next_page': '/'}, name='mysite_logout'),
)

# Model retrieval - former used by jquery
urlpatterns += patterns('',
    url(r'^gremium/list$', login_required(list_gremien), name='list_gremien'),
    url(r'^vorhaben/list$', login_required(list_vorhaben), name='list_vorhaben'),
    url(r'^nachrichten/list$', login_required(list_nachrichten),
        name='list_nachrichten'),
)

