from django.test import TestCase
from django.conf import settings
import graphviz as gv
from .models import Graph
from django.core.files import File
import os
import shutil


class TestInit(TestCase):
	def test_media_root(self):
		self.assertEqual('C:\\github\\energy_network\\media_cdn', settings.MEDIA_ROOT)

	def test_media_url(self):
		self.assertEqual('/media/', settings.MEDIA_URL)


class TestRenderGraph(TestCase):
	def setUp(self):
		self.filename = 'test_1'
		self.render_path = 'media/' + self.filename
		self.test_1 = init_graph()

	def tearDown(self):
		if os.path.exists(self.filepath):
			os.remove(self.render_path)
			os.remove(self.filepath)
		directory = os.path.join(settings.MEDIA_ROOT, 'graph_1')
		if os.path.exists(directory):
			shutil.rmtree(directory)

	def test_filename_and_render_filepath(self):
		self.filepath = render_graph(self.test_1, self.render_path)
		self.assertEqual('media/test_1.png', self.filepath)
		self.assertTrue(os.path.exists(self.render_path))
		self.assertTrue(os.path.exists(self.filepath))

	def test_save_model(self):
		self.filepath = render_graph(self.test_1, self.render_path)	
		saved_graph = save_graph(self.filename, self.filepath)
		self.assertEqual('/media/graph_1/test_1.png', saved_graph.image.url)
		self.assertEqual(
			'C:\\github\\energy_network\\media_cdn\\graph_1\\test_1.png',
			os.path.join(settings.MEDIA_ROOT, 'graph_1', self.filename + '.png'))


def init_graph(format='png'):
	graph = gv.Graph(format=format)
	graph.node('A')
	graph.node('B')
	graph.edge('A', 'B')
	return graph

def render_graph(gv_graph, filename):
	return gv_graph.render(filename=filename)

def save_graph(filename, render_path, image_format='png'):
	Graph(title=filename).save()
	g = Graph.objects.get(title=filename)
	django_file = File(open(render_path, 'rb'))
	file = '{}.{}'.format(filename, image_format)
	g.image.save(file, django_file, save=True)
	return Graph.objects.get(title=filename)
