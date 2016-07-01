from .domain import GraphRender
from .models import Graph
from .forms import GraphForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os

def graphs_list(request):
	paginator_page_var = 'page'
	paginator_count = 5
	queryset_list = Graph.objects.all()
	paginator = Paginator(queryset_list, paginator_count)
	page = request.GET.get(paginator_page_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)
	new_graph = Graph()
	context = {
		'posts': queryset,
		'paginator_page_var': paginator_page_var,
		'new_post': new_graph,
	}
	return render(request, 'posts_list.html', context)

def graph_details(request, pk=0):
	graph = get_object_or_404(Graph, pk=pk)
	context = { 
		'post': graph,
	}
	return render(request, 'post_details.html', context)

def graph_create(request, test=False):
	form = GraphForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		title = request.POST.get('title', '')
		csv_file = request.FILES.get('csv_file', '')

		if not title:
			title = 'empty'

		g = Graph(title=title)
		g.save()

		if not csv_file:
			csv_file = 'empty.csv'

		g.csv_file = csv_file
		g.save()

		s = g.csv_file.url[1:]

		img = g.render_from_csv(csv_source=s, render_format='svg')
		g.image = img.replace('media/', '')
		g.save()

		s = 'media/graph_'+str(g.pk)+'/graph.svg'

		return HttpResponseRedirect(g.get_details_url())
	context = { 'form': form, 'test': test }
	return render(request, 'post_form.html', context)

def graph_update(request, pk=0, test=False):
	instance = get_object_or_404(Graph, pk=pk)
	form = GraphForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		title = request.POST.get('title', '')
		csv_file = request.FILES.get('csv_file', '')

		instance.title = title
		instance.render_and_save_from_csv(
			csv_source=csv_file.name, 
			render_format='svg')

		return HttpResponseRedirect(instance.get_details_url())
	context = {'form': form, 'test': test,}
	return render(request, 'post_form.html', context)

def graph_delete(request, pk=0):
	instance = get_object_or_404(Graph, pk=pk)
	instance.delete()
	return redirect('graphs:list')
