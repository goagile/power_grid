from django.conf.urls import url
from .views import (
	graphs_list,
	graph_details,
	graph_create,
	graph_update,
	graph_delete,
)

urlpatterns = [
	url(r'^$', graphs_list, name='list'),
	url(r'^create/$', graph_create, name='create'),
	url(r'^(?P<pk>\d+)/$', graph_details, name='details'),
	url(r'^(?P<pk>\d+)/update/$', graph_update, name='update'),
	url(r'^(?P<pk>\d+)/delete/$', graph_delete, name='delete'),
]
