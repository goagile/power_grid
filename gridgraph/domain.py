import os
import shutil
import csv
import graphviz as gv
from django.conf import settings
from django.core.files import File
from .models import Graph


class GraphRender:
	def __init__(self, filename, gv_graph=None, render_dir='media', render_format='png'):
		self.filename = filename
		self.render_format = render_format
		self.dotfile = '{}/{}'.format(render_dir, filename)
		self.filepath = '{}.{}'.format(self.dotfile, self.render_format)

		self.csv_filepath = '{}.{}'.format(self.dotfile, 'csv')

		self.file = '{}.{}'.format(filename, render_format)
		self.csv_file = '{}.{}'.format(filename, 'csv')

		self.media_dir = ''
		self.media_filepath = ''
		if not gv_graph:
			self.gv_graph = self.default_gv_graph()

	def default_gv_graph(self):
		graph = gv.Graph(format=self.render_format)
		graph.attr('node', shape='circle')
		graph.node('A')
		graph.node('B')
		graph.edge('A', 'B')
		return graph

	def render(self):
		return self.gv_graph.render(filename=self.dotfile)

	def clear_filepath(self):
		if os.path.exists(self.filepath):
			os.remove(self.dotfile)
			os.remove(self.filepath)
		if os.path.exists(self.media_dir):
			shutil.rmtree(self.media_dir)

	def save(self):
		Graph(title=self.filename).save()
		instance = Graph.objects.get(title=self.filename)
		
		image = File(open(self.filepath, 'rb'))
		instance.image.save(self.file, image, save=True)
		
		if os.path.exists(self.csv_filepath):
			csv_file = File(open(self.csv_filepath, 'rb'))
			instance.csv_file.save(self.csv_file, csv_file, save=True)

		self.subdir_pk = '{}_{}'.format(Graph.media_subdir, instance.pk)
		self.media_dir = os.path.join(settings.MEDIA_ROOT, self.subdir_pk)
		self.media_filepath = os.path.join(self.media_dir, self.file)
		return instance

	def init_from_csv(self, filename):
		self.gv_graph = self.create_from_csv(filename)

	def create_from_csv(self, filename):
		result = self.read_csv(filename)
		nodes, edges = result['nodes'], result['edges']
		gv_graph = gv.Graph(format=self.render_format)
		gv_graph.attr('node', shape='circle')
		for node in nodes:
			gv_graph.node(node)
		for edge in edges:
			gv_graph.edge(edge[0], edge[1])
		return gv_graph

	def read_csv(self, filename):
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