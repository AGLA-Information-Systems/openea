import os

from django.test import TestCase

from ontology.controllers.graphviz import GraphvizController
from utils.test.helpers import populate_test_env

__author__ = "Patrick Agbokou"
__copyright__ = "Copyright 2021, OpenEA"
__credits__ = ["Patrick Agbokou"]
__license__ = "Apache License 2.0"
__version__ = "1.0.0"
__maintainer__ = "Patrick Agbokou"
__email__ = "patrick.agbokou@aglaglobal.com"
__status__ = "Development"


class GraphvizControllerTestCase(TestCase):
    def setUp(self):
        populate_test_env(self)

    def test_build_svg(self):
        svg = GraphvizController.render_model_graph(format='svg', model=self.org_1_model_1)
        self.assertEqual(svg, '', svg)
#TODO