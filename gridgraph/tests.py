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


# class TestGraphFromCSV(TestCase):
# 	def setUp(self):
# 		self.gr = GraphRender(filename='test_csv')
# 		self.gr.from_csv(csv_filename)
# 		self.gr.render()

# 	def tearDown(self):
# 		self.gr.clear_filepath()

# 	def test_(self):
# 		self.assertEqual('media/test_csv.png', self.gr.filepath)


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

	def test_from_csv(self):
		result = read_csv(self.filename)
		self.assertEqual(sorted(self.fixture['nodes']), sorted(result['nodes']))
		self.assertEqual(sorted(self.fixture['edges']), sorted(result['edges']))

	def test_init_from_csv(self):
		gv_graph = init_from_csv(self.filename)
		for node in self.fixture['nodes']:
			self.assertIn(node, gv_graph.source)
		for edge in self.fixture['edges']:
			self.assertIn(edge[0]+' -- '+edge[1], gv_graph.source)

def init_from_csv(filename):
	result = read_csv(filename)
	nodes, edges = result['nodes'], result['edges']
	gv_graph = gv.Graph(format='png')
	gv_graph.attr('node', shape='circle')
	for node in nodes:
		gv_graph.node(node)
	for edge in edges:
		gv_graph.edge(edge[0], edge[1])
	return gv_graph

def read_csv(filename):
	result = {'nodes': [], 'edges': [],}
	with open(filename, 'r', newline='') as f:
		reader = csv.reader(f); next(reader, None); next(reader, None)
		for line in reader:
			if line[0]:
				result['nodes'].append(line[0])
			if line[1] and line[2]:
				result['edges'].append((line[1], line[2]))
	result['nodes'] = list(set(result['nodes']))
	return result
