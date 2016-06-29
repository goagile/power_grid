import os
import csv
import graphviz as gv
from django.test import TestCase
from django.conf import settings
from .domain import GraphRender


class TestInit(TestCase):
	def test_media_root(self):
		self.assertEqual('C:\\github\\energy_network\\media_cdn', settings.MEDIA_ROOT)

	def test_media_url(self):
		self.assertEqual('/media/', settings.MEDIA_URL)


class TestGraphRender(TestCase):
	def setUp(self):
		self.gr = GraphRender(filename='test_1')
		self.gr.render()

	def tearDown(self):
		self.gr.clear_filepath()

	def test_filename_and_render_filepath(self):
		self.assertEqual('media/test_1.png', self.gr.filepath)
		self.assertTrue(os.path.exists(self.gr.dotfile))
		self.assertTrue(os.path.exists(self.gr.filepath))

	def test_save_model(self):
		instance = self.gr.save()
		self.assertEqual('/media/graph_1/test_1.png', instance.image.url)
		self.assertEqual('C:\\github\\energy_network\\media_cdn\\graph_1\\test_1.png',
			self.gr.media_filepath)


class TestCSV(TestCase):
	filename = 'test.csv'
	csv_lines = [
		'Узлы,Ветки,\n',
		'Номер,Узел 1,Узел 2\n',
		'0,0,1\n',
		'1,0,2\n',
		'2,1,2\n',
		'0,2,1\n',
		'1,,\n',
	]
	fixture = {
		'nodes': ['0','1','2'],
		'edges': [
			('0', '1',),
			('0', '2',),
			('1', '2',),
			('2', '1',),
		],
	}
	gv_source = """
		graph {
		      node [shape=circle]
		      0
		      2
		      1
		              0 -- 1
		              0 -- 2
		              1 -- 2
		              2 -- 1
		}"""

	def setUp(self):
		with open(self.filename, 'w') as f:
			for line in self.csv_lines:
				f.write(line)

	def tearDown(self):
		if os.path.exists(self.filename):
			os.remove(self.filename)

	def test_read_csv(self):
		gr = GraphRender(filename='test')
		result = gr.read_csv(self.filename)
		self.assertEqual(sorted(self.fixture['nodes']), sorted(result['nodes']))
		self.assertEqual(sorted(self.fixture['edges']), sorted(result['edges']))

	def test_init_from_csv(self):
		gr = GraphRender(filename='test')
		gr.init_from_csv(self.filename)
		source = gr.gv_graph.source
		for node in self.fixture['nodes']:
			self.assertIn(node, source)
		for edge in self.fixture['edges']:
			self.assertIn(edge[0]+' -- '+edge[1], source)


class TestUseCSV(TestCase):
	test_filepath = 'media/testo.csv'
	csv_lines = [
		'Узлы,Ветки,\n',
		'Номер,Узел 1,Узел 2\n',
		'0,0,1\n',
		'1,0,2\n',
		'2,1,2\n',
		'0,2,1\n',
		'1,,\n',
	]

	def setUp(self):
		self.gr = GraphRender(filename='testo')
		with open(self.test_filepath, 'w') as f:
			for line in self.csv_lines:
				f.write(line)
		self.gr.init_from_csv(self.test_filepath)

	def tearDown(self):
		self.gr.clear_filepath()
		if os.path.exists(self.test_filepath):
			os.remove(self.test_filepath)

	def test_init_from_csv(self):
		self.assertTrue(os.path.exists(self.test_filepath))
		self.assertEqual('media/testo.png', self.gr.filepath)
		self.assertEqual('media/testo.csv', self.gr.csv_filepath)

	def test_save_model_and_csv(self):
		self.gr.render()
		instance = self.gr.save()
		self.assertEqual('/media/graph_1/testo.png', instance.image.url)
		self.assertEqual('/media/graph_1/testo.csv', instance.csv_file.url)
