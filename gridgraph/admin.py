from django.contrib import admin
from .models import Graph

class GraphModelAdmin(admin.ModelAdmin):
	search_fields = ['title']
	list_display_links = ['title']
	list_display = ['title', 'publish', 'image', 'csv_file',]
	class Meta:
		model = Graph

admin.site.register(Graph, GraphModelAdmin)
