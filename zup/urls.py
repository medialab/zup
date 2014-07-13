from django.conf.urls import patterns, include, url
from django.contrib import admin



admin.autodiscover()



apipatterns = patterns('zup.api',
  url(r'^$', 'home', name='zup_api_home'),
  
  url(r'^job$', 'jobs', name='zup_api_jobs'),
  url(r'^job/(?P<pk>\d+)$', 'job', name='zup_api_job'),
  url(r'^job/(?P<pk>\d+)/download$', 'job_download', name='zup_api_job_download'),
)

urlpatterns = patterns('',
    url(r'^$', 'zup.views.home', name='home'),
    url(r'^api/', include(apipatterns)),

    url(r'^admin/', include(admin.site.urls)),
)
