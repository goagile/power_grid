from django.test import TestCase
from django.conf import settings
import graphviz as gv
from .models import Graph
from django.core.files import File
import os
import shutil


class TestInit(TestCase):
	def test_media_root(self):
		self.assertEqual('C:\github\energy_network\media_cdn', settings.MEDIA_ROOT)

	def test_media_url(self):
		self.assertEqual('/media/', settings.MEDIA_URL)


class TestRenderGraph(TestCase):
	def setUp(self):
		self.test_1 = get_gv_graph()

	def tearDown(self):
		if os.path.exists(self.filepath):
			os.remove(self.filename)
			os.remove(self.filepath)

	def test_filename_and_render_filepath(self):
		self.filename = 'media/test_1'
		self.filepath = self.test_1.render(filename=self.filename)
		self.assertEqual('media/test_1.png', self.filepath)
		self.assertTrue(os.path.exists(self.filename))
		self.assertTrue(os.path.exists(self.filepath))

	def test_save_model(self):
		self.filename = 'media/test_1'
		self.filepath = self.test_1.render(filename=self.filename)	
		Graph(title='test_1').save()
		g = Graph.objects.get(title='test_1')
		g.image.save('test_1.png', File(open(self.filepath, 'rb')), save=True)
		saved_graph = Graph.objects.get(title='test_1')
		self.assertEqual('/media/graph_1/test_1.png', saved_graph.image.url)
		self.assertEqual(
			'C:\\github\\energy_network\\media_cdn\\graph_1\\test_1.png',
			os.path.join(settings.MEDIA_ROOT, 'graph_1', 'test_1.png'))
		# 
		file = os.path.join(settings.MEDIA_ROOT, 'graph_1', 'test_1.png')
		directory = os.path.join(settings.MEDIA_ROOT, 'graph_1')
		shutil.rmtree(directory)


def get_gv_graph(format='png'):
	graph = gv.Graph(format=format)
	graph.node('A')
	graph.node('B')
	graph.edge('A', 'B')
	return graph