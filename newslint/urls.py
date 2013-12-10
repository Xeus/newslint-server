from django.conf.urls import patterns, include, url
from django.contrib import admin
import views
import api_views
admin.autodiscover()


urlpatterns = patterns('',

    # public routes
    url(r'^$', views.index, name='index'),
    url(r'^lint/', views.input_clipping, name='input_clipping'),  # user form to add clipping
    url(r'^post/', views.lint_clipping, name='lint_clipping'),  # handles POST request
    url(r'^result/', views.lint_result, name='lint_result'),
    url(r'^clippings/', include('linter.urls')),
    # url(r'^api/v1/clippings/', include('linter.urls')),

    # public API routes
    url(r'^' + api_views.API_PREFIX + '$', api_views.index, name='api_index'),
    url(r'^' + api_views.API_PREFIX + r'linter/$', api_views.linter, name='api_linter'),
    url(r'^' + api_views.API_PREFIX + r'linter(?:/|)?q=\w*$', api_views.linter, name='api_linter'),
    url(r'^' + api_views.API_PREFIX + r'help/', api_views.help, name='api_help'),

    # admin routes
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
