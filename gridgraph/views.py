from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import graphviz as gv
from .models import Graph
from django.core.files import File

# IMG_URL = '/media/'

def graph(request):
	# читаем настройки ...
	# строим граф
	graph_name = 'test_1'
	graph_img_format = 'png'
	graph_filename = '{}.{}'.format(graph_name, graph_img_format)
	test_1 = gv.Graph(format=graph_img_format)
	test_1.node('A')
	test_1.node('B')
	test_1.edge('A', 'B')
	# # сохраняем изображение графа
	filename = settings.MEDIA_URL + graph_name
	filepath = test_1.render(filename=filename)
	# загружаем изображение графа
	with open(filepath, 'rb') as f:
		g = Graph()
		g.title=graph_name
		g.image.save(graph_filename, File(f), save=True)
	# возвращаем ответ браузеру
	return HttpResponse(filepath)