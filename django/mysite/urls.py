from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from fraktionstool.views import VorhabenView
from fraktionstool.views import list_gremien

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', login_required(VorhabenView.as_view()), name='home'),
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

# Model retrieval
urlpatterns += patterns('',
    url(r'^gremium/list$', list_gremien, name='list_gremien'),
)

