from .domain import GraphRender
from .models import Graph
from .forms import GraphForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
	# graph = get_object_or_404(Graph, pk=pk)
	gr = GraphRender(filename='zgraph', render_format='png')
	gr.init_from_csv('z.csv')
	gr.render()
	graph = gr.save()
	
	image = graph.image.url
	
	context = { 
		'post': graph,
		'image': image,
	}
	return render(request, 'post_details.html', context)

	# gr = GraphRender(filename='zgraph', render_format='svg')
	# gr.init_from_csv('media/zgraph.csv')
	# gr.render()
	# gr.save()
	# return HttpResponse(gr.gv_graph.pipe().decode())

def graph_create(request, test=False):
	form = GraphForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(instance.get_details_url())
	context = { 'form': form, 'test': test }
	return render(request, 'post_form.html', context)


def graph_update(request, pk=0, test=False):
	instance = get_object_or_404(Graph, pk=pk)
	form = GraphForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(instance.get_details_url())
	context = {'form': form, 'test': test,}
	return render(request, 'post_form.html', context)


def graph_delete(request, pk=0):
	instance = get_object_or_404(Graph, pk=pk)
	instance.delete()
	return redirect('graphs:list')
