from django.db import models


def upload_location(instance, filename):
	return '{}_{}/{}'.format(Graph.media_subdir, instance.pk, filename)


class Graph(models.Model):
	media_subdir = 'graph'
	title = models.CharField(max_length=120)
	image = models.ImageField(
		upload_to=upload_location,
		null=True, 
		blank=True,
		width_field='width_field',
		height_field='height_field',)
	width_field = models.IntegerField(default=0)
	height_field = models.IntegerField(default=0)
	publish = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __str__(self):
		return self.title