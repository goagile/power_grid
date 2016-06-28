import os
from django.test import TestCase
from django.conf import settings
from .domain import GraphRender


class TestInit(TestCase):
	def test_media_root(self):
		self.assertEqual('C:\\github\\energy_network\\media_cdn', settings.MEDIA_ROOT)

	def test_media_url(self):
		self.assertEqual('/media/', settings.MEDIA_URL)


class TestRenderGraph(TestCase):
	def setUp(self):
		self.gr = GraphRender(filename='test_1', render_dir='media')

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
