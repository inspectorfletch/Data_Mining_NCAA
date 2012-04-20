from django.conf.urls.defaults import patterns, include, url
from data_mining.NCAA.views import *

urlpatterns = patterns(
	'NCAA.views',
	(r'^NCAA/$', index),
	(r'^NCAA/simulate/$', simulate),
)