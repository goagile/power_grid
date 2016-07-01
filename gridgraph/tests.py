import os
import shutil
import csv
import graphviz as gv
from django.test import TestCase
from django.conf import settings
from .domain import GraphRender
from .models import Graph, upload_location
from django.core.files import File


class TestInit(TestCase):
	def test_base_dir(self):
		self.assertEqual(
			'C:\\github\\energy_network\\src', 
			settings.BASE_DIR)

	def test_media_root(self):
		self.assertEqual(
			'C:\\github\\energy_network\\src\\media', 
			settings.MEDIA_ROOT)

	def test_media_url(self):
		self.assertEqual('/media/', settings.MEDIA_URL)


class TestUploadLocation(TestCase):
	def setUp(self):
		self.csv_filename = 'test.csv'
		self.g = Graph(title='test')

	def test_upload_location(self):
		self.g.save()
		upload_to = upload_location(instance=self.g, filename=self.csv_filename)
		self.assertEqual('graph_1/test.csv', upload_to)

	def test_save_and_create_graph_model_pk(self):
		self.assertEqual(None, self.g.pk)
		self.g.save()
		self.assertEqual(1, self.g.pk)
		self.assertEqual(1, Graph.objects.count())


class TestSaveFiles(TestCase):
	test_csv = 'test.csv'
	
	def create_test_csv(self):
		with open(self.test_csv, 'w') as f:
			for line in self.csv_lines:
				f.write(line)

	def setUp(self):
		self.g = Graph(title='test', name='test')
		self.csv_lines = [
			'Узлы,Ветки,\n',
			'Номер,Узел 1,Узел 2\n',
			'0,0,1\n',
			'1,0,2\n',
			'2,1,2\n',
			'0,2,1\n',
			'1,,\n',
		]
		self.create_test_csv()

	def tearDown(self):
		# if os.path.exists('media'):
		# 	shutil.rmtree('media')
		# os.mkdir('media')
		if os.path.exists(self.test_csv):
			os.remove(self.test_csv)

	def test_render_img_from_csv(self):
		g = self.g
		g.save()
		g.save_csv_file(self.test_csv)
		self.assertEqual('/media/graph_1/test.csv', g.csv_file.url)
		self.assertEqual('media/graph_1/test', g.get_dotpath())
		self.assertTrue(os.path.exists('media/graph_1/test.csv'))

		img = g.render_from_csv(csv_source='media/graph_1/test.csv',
			render_format='png')
		self.assertEqual(g.get_dotpath()+'.png', img)
		self.assertTrue(os.path.exists(g.get_dotpath()+'.png'))

	def test_render_and_save_from_csv(self):
		g = self.g

		g.render_and_save_from_csv(
			csv_source=self.test_csv,
			render_format='png')

		self.assertEqual('/media/graph_1/test.csv', g.csv_file.url)
		self.assertEqual('media/graph_1/test', g.get_dotpath())
		self.assertTrue(os.path.exists('media/graph_1/test.csv'))
		self.assertTrue(os.path.exists(g.get_dotpath()+'.png'))
