from django.db import models
from django.core.urlresolvers import reverse


def upload_location(instance, filename):
	return '{}_{}/{}'.format(Graph.media_subdir, instance.id, filename)


class Graph(models.Model):
	media_subdir = 'graph'
	title = models.CharField(max_length=120)
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

	def get_graph_image(self):
		if self.csv_file:
			return True
		return False