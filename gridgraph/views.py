# from django.shortcuts import render
from django.http import HttpResponse
from .domain import GraphRender


def graph(request):
	g = GraphRender(filename='test_1', render_format='svg')
	# g.save()
	return HttpResponse(g.gv_graph.pipe().decode())
	# return HttpResponse(gv.pipe().decode('utf-8'))