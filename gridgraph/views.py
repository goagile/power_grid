from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import graphviz as gv


def graph(request):
	# g1 = gv.Graph(format='svg')
	# g1.node('A')
	# g1.node('B')
	# g1.edge('A', 'B')
	# filename = g1.render(filename=settings.MEDIA_ROOT + '\g1')
	# template = '<img src="{}"/>'
	# return HttpResponse(template.format(filename))
	return HttpResponse(template.format(filename))