from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from fraktionstool.views import NachrichtenList, HilfeList
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
    url(r'^hilfe/', HilfeList.as_view(template_name='hilfe.html'))
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', {'template_name': 'login.html'},
        name='mysite_login'),
    url(r'^logout/$', 'logout', {'next_page': '/'}, name='mysite_logout'),
    url(r'^accounts/password_change/$', 'password_change',
            {'template_name': 'password_change.html'}, name='change_password'),
    url(r'^accounts/password_change/done/$', 'password_change_done',
            {'template_name': 'password_change_done.html'},
            name='password_change_done'),
)

# Model retrieval - former used by jquery
urlpatterns += patterns('',
    url(r'^gremium/list$', login_required(list_gremien), name='list_gremien'),
    url(r'^vorhaben/list$', login_required(list_vorhaben), name='list_vorhaben'),
    url(r'^nachrichten/list$', login_required(list_nachrichten),
        name='list_nachrichten'),
)

