from django.conf.urls import patterns, include, url
from django.contrib import admin
import views
import api_views
admin.autodiscover()


urlpatterns = patterns('',

    # public routes
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^lint/', views.lint, name='lint'),  # user form to add clipping
    url(r'^post/', views.lint_clipping, name='lint_clipping'),  # handles POST request
    url(r'^result/', views.lint_result, name='lint_result'),
    url(r'^clippings/$', views.list, name='list'),
    url(r'^clipping/(?P<pk>\d+)/$', views.detail, name='detail'),

    # public API routes
    url(r'^' + api_views.API_PREFIX + '$', api_views.help, name='api_index'),
    url(r'^' + api_views.API_PREFIX + r'linter/$', api_views.linter, name='api_linter'),
    url(r'^' + api_views.API_PREFIX + r'clipping/(?P<pk>\d+)/$$', api_views.detail, name='api_detail'),
    url(r'^' + api_views.API_PREFIX + r'clippings/$', api_views.list, name='api_list'),
    url(r'^' + api_views.API_PREFIX + r'post/$', api_views.lint_and_save, name='api_lint_and_save'),
    url(r'^' + api_views.API_PREFIX + r'linter(?:/|)?content=\w*$', api_views.linter, name='api_linter'),
    url(r'^' + api_views.API_PREFIX + r'help/', api_views.help, name='api_help'),

    # admin routes
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
