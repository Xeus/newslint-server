from django.conf.urls import patterns, include, url
from django.contrib import admin
import views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^lint/', views.input_clipping, name='input_clipping'),  # user form to add clipping
    url(r'^post/', views.lint_clipping, name='lint_clipping'),  # handles POST request
    url(r'^result/', views.lint_result, name='lint_result'),
    url(r'^clippings/', include('linter.urls')),
    # url(r'^api/v1/clippings/', include('linter.urls')),
    url(r'^api/v1/linter/', views.linter, name='linter'),
    url(r'^api/v1/help/', views.api_help, name='help'),
    url(r'^$', views.index, name='index'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
