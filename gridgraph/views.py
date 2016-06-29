# from django.shortcuts import render
from django.http import HttpResponse
from .domain import GraphRender


def graph(request):
	gr = GraphRender(render_format='svg')
	gr.init_from_csv('test.csv')
	return HttpResponse(gr.gv_graph.pipe().decode())
