import os

from django.test import TestCase

from ontology.controllers.graphviz import GraphvizController
from utils.test.helpers import populate_test_env


class GraphvizControllerTestCase(TestCase):
    def setUp(self):
        populate_test_env(self)

    def test_build_svg(self):
        svg = GraphvizController.render_model_graph(format='svg', model=self.org_1_model_1)
        self.assertEqual(svg, '', svg)
#TODO