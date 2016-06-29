from django.db import models


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

	def __str__(self):
		return self.title
		