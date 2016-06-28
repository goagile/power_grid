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
		self.gr = GraphRender(filename='test_1', render_dir='media')

	def tearDown(self):
		if os.path.exists(self.filepath):
			os.remove(self.gr.render_path)
			os.remove(self.filepath)
		directory = os.path.join(settings.MEDIA_ROOT, 'graph_1')
		if os.path.exists(directory):
			shutil.rmtree(directory)

	def test_filename_and_render_filepath(self):
		self.filepath = self.gr.render()
		self.assertEqual('media/test_1.png', self.filepath)
		self.assertTrue(os.path.exists(self.gr.render_path))
		self.assertTrue(os.path.exists(self.filepath))

	def test_save_model(self):
		self.filepath = self.gr.render()	
		saved_graph = self.gr.save(self.filepath)
		self.assertEqual('/media/graph_1/test_1.png', saved_graph.image.url)
		self.assertEqual(
			'C:\\github\\energy_network\\media_cdn\\graph_1\\test_1.png',
			os.path.join(settings.MEDIA_ROOT, 'graph_1', self.gr.filename + '.png'))


class GraphRender:
	def __init__(self, filename, render_dir):
		self.gv_graph = self.init()
		self.filename = filename
		self.render_path = render_dir + '/' + filename

	def init(self, format='png'):
		graph = gv.Graph(format=format)
		graph.node('A')
		graph.node('B')
		graph.edge('A', 'B')
		return graph

	def render(self):
		return self.gv_graph.render(filename=self.render_path)

	def save(self, render_path, image_format='png'):
		Graph(title=self.filename).save()
		g = Graph.objects.get(title=self.filename)
		django_file = File(open(render_path, 'rb'))
		file = '{}.{}'.format(self.filename, image_format)
		g.image.save(file, django_file, save=True)
		return Graph.objects.get(title=self.filename)
