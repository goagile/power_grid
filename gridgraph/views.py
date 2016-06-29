# from django.shortcuts import render
from django.http import HttpResponse
from .domain import GraphRender


def graph(request):
	gr = GraphRender(filename='zgraph', render_format='svg')
	gr.init_from_csv('media/zgraph.csv')
	gr.render()
	gr.save()
	return HttpResponse(gr.gv_graph.pipe().decode())
