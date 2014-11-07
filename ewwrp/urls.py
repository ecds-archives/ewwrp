from django.conf.urls import patterns, include, url
from ewwrp.views import *

#from django.contrib import admin
#admin.autodiscover()

# Something needs to be done to make this better.

urlpatterns = patterns('ewwrp/views',
	url(r'^about/$', about, name='about'),
    url(r'^(?P<app>\w+)/about/$', about, name='about'),
    
    url(r'^(?P<app>\w+)/essays/$', essays, name='essays'),
    url(r'^(?P<app>\w+)/essays/(?P<essay_id>)/', essays, name='essays'),
    
    url(r'^(?P<app>\w+)/browse/$', browse, name='browse'),
    
    url(r'^(?P<app>\w+)/search/$', search, name='search'),
    
    url(r'^(?P<app>\w+)/advancedsearch/$', search, {'method': 'advanced'}, name='advsearch'),
    
    url(r'^(?P<app>\w+)/view/(?P<doc_id>.+)/(?P<page>.+)/$', page, name='page'),
        
    url(r'^$', index, name='index'),
    url(r'^(?P<app>\w+)/$', index, name='index'),
)