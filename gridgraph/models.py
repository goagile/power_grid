from django.db import models
from django.core.urlresolvers import reverse
import os
import csv
from django.core.files import File
from django.conf import settings
import graphviz as gv

def upload_location(instance, filename=''):
	media_subdir_id = '{}_{}'.format(Graph.media_subdir, instance.id)
	return '{}/{}'.format(media_subdir_id, filename)


class Graph(models.Model):
	media_subdir = 'graph'
	name = models.CharField(max_length=120, default='graph')
	title = models.CharField(max_length=120, null=True, blank=True)
	csv_file = models.FileField(
		upload_to=upload_location,
		null=True, 
		blank=True,)
	image = models.ImageField(
		upload_to=upload_location,
		null=True, 
		blank=True,)
	publish = models.DateTimeField(auto_now=False, auto_now_add=True)

	class Meta:
		ordering = ['-publish',]

	def __str__(self):
		return self.title
	
	def get_details_url(self):
		return reverse('graphs:details', kwargs={ 'pk': self.pk })

	def get_create_url(self):
		return reverse('graphs:create')	

	def get_list_url(self):
		return reverse('graphs:list')

	def get_update_url(self):
		return reverse('graphs:update', kwargs={ 'pk': self.pk })

	def get_delete_url(self):
		return reverse('graphs:delete', kwargs={ 'pk': self.pk })		

	def save_csv_file(self, source):
		if os.path.exists(source):
			with open(source, 'rb') as f:
				filename=self.name+'.csv'
				self.csv_file.save(filename, File(f))

	def save_image_file(self, source, file_format='.svg'):
		if os.path.exists(source):
			with open(source, 'rb') as f:
				filename = self.name + file_format
				self.image.save(filename, File(f))

	def get_dotpath(self):
		return '{}{}{}'.format(
			settings.MEDIA_URL[1:],
			upload_location(self),
			self.name,)

	def render_and_save_from_csv(self, csv_source=None, render_format='svg'):
		self.save()
		self.save_csv_file(csv_source)
		img = self.render_from_csv(render_format=render_format)
		self.image = img.replace('media/', '')
		self.save()

	def render_from_csv(self, csv_source=None, render_format='svg'):

		if not csv_source:
			csv_source = self.get_dotpath()+'.csv'

		gv_graph = self.create_from_csv(filename=csv_source, 
			render_format=render_format)
		img = gv_graph.render(filename=self.get_dotpath())
		return img

	def create_from_csv(self, filename, render_format='svg'):
		result = self.read_csv(filename)
		nodes, edges = result['nodes'], result['edges']
		gv_graph = gv.Graph(format=render_format)
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