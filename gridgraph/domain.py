import os
import shutil
import graphviz as gv
from django.conf import settings
from django.core.files import File
from .models import Graph


class GraphRender:
	def __init__(self, filename, render_dir, render_format='png'):
		self.filename = filename
		self.render_format = render_format
		self.dotfile = '{}/{}'.format(render_dir, filename)
		self.filepath = '{}.{}'.format(self.dotfile, self.render_format)
		self.file = '{}.{}'.format(filename, render_format)
		self.gv_graph = self.init()
		self.media_dir = ''
		self.media_filepath = ''
		self.render()

	def init(self):
		graph = gv.Graph(format=self.render_format)
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
		django_file = File(open(self.filepath, 'rb'))
		instance = Graph.objects.get(title=self.filename)
		instance.image.save(self.file, django_file, save=True)
		self.subdir_pk = '{}_{}'.format(Graph.media_subdir, instance.pk)
		self.media_dir = os.path.join(settings.MEDIA_ROOT, self.subdir_pk)
		self.media_filepath = os.path.join(self.media_dir, self.file)
		return instance
