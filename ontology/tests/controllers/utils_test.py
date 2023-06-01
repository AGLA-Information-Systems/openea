import os

from django.test import TestCase
from openpyxl import load_workbook

from ontology.controllers.utils import DEFAULT_MAX_LEVEL, KnowledgeBaseUtils
from utils.test.helpers import populate_test_env

__author__ = "Patrick Agbokou"
__copyright__ = "Copyright 2021, OpenEA"
__credits__ = ["Patrick Agbokou"]
__license__ = "Apache License 2.0"
__version__ = "1.0.0"
__maintainer__ = "Patrick Agbokou"
__email__ = "patrick.agbokou@aglaglobal.com"
__status__ = "Development"


class KnowledgeBaseUtilsTestCase(TestCase):
    def setUp(self):
        populate_test_env(self)

    def test_get_parent_concepts(self):
        parent_concepts = KnowledgeBaseUtils.get_parent_concepts(concept=self.org_1_concept_4)
        self.assertEqual(len(parent_concepts), 2, parent_concepts)
        self.assertEqual(parent_concepts[0][0], self.org_1_concept_1, parent_concepts)
        self.assertEqual(parent_concepts[0][1], 0, parent_concepts)
        self.assertEqual(parent_concepts[1][0], self.org_1_concept_0, parent_concepts)
        self.assertEqual(parent_concepts[1][1], 1, parent_concepts)

    def test_get_recursive_parent_concepts(self):
        parent_concepts = KnowledgeBaseUtils.get_recursive_parent_concepts(concept=self.org_1_concept_4, results=[], level=0, max_level=100)
        self.assertEqual(len(parent_concepts), 2, parent_concepts)
        self.assertEqual(parent_concepts[0][0], self.org_1_concept_1, parent_concepts)
        self.assertEqual(parent_concepts[0][1], 0, parent_concepts)
        self.assertEqual(parent_concepts[1][0], self.org_1_concept_0, parent_concepts)
        self.assertEqual(parent_concepts[1][1], 1, parent_concepts) 

    def test_get_child_concepts(self):
        child_concepts = KnowledgeBaseUtils.get_child_concepts(concept=self.org_1_concept_0)
        self.assertEqual(len(child_concepts), 2, child_concepts)
        self.assertEqual(child_concepts[0][0], self.org_1_concept_1, child_concepts)
        self.assertEqual(child_concepts[0][1], 0, child_concepts)
        self.assertEqual(child_concepts[1][0], self.org_1_concept_4, child_concepts)
        self.assertEqual(child_concepts[1][1], 1, child_concepts)

    def test_get_recursive_child_concepts(self):
        child_concepts = KnowledgeBaseUtils.get_recursive_child_concepts(concept=self.org_1_concept_0, results=[], level=0, max_level=100)
        self.assertEqual(len(child_concepts), 2, child_concepts)
        self.assertEqual(child_concepts[0][0], self.org_1_concept_1, child_concepts)
        self.assertEqual(child_concepts[0][1], 0, child_concepts)
        self.assertEqual(child_concepts[1][0], self.org_1_concept_4, child_concepts)
        self.assertEqual(child_concepts[1][1], 1, child_concepts)  


    def test_get_related_object_concepts(self):
        predicate_ids = None
        concepts = KnowledgeBaseUtils.get_related_object_concepts(concept=self.org_1_concept_1, predicate_ids=predicate_ids)
        self.assertEqual(len(concepts), 4, concepts)
        self.assertIn((self.org_1_concept_0, 0), concepts, concepts)
        self.assertIn((self.org_1_concept_3, 1), concepts, concepts)
        concepts = KnowledgeBaseUtils.get_related_object_concepts(concept=self.org_1_concept_1, predicate_ids=predicate_ids, max_level=0)
        self.assertEqual(len(concepts), 3, concepts)
        self.assertIn((self.org_1_concept_0, 0), concepts, concepts)

    def test_get_related_subject_concepts(self):
        predicate_ids = None
        concepts = KnowledgeBaseUtils.get_related_subject_concepts(concept=self.org_1_concept_2, predicate_ids=predicate_ids)
        self.assertEqual(len(concepts), 1, concepts)
        self.assertIn((self.org_1_concept_1, 0), concepts, concepts)

    def test_get_instances_paths(self):
        paths = KnowledgeBaseUtils.get_instances_paths(start_instance=self.org_1_instance_1, end_instance=self.org_1_instance_3)
        best_path = (100, [])
        if not paths.empty():
            best_path = paths.get()
        self.assertEqual(best_path[0], 2, best_path[1])

        paths = KnowledgeBaseUtils.get_instances_paths(start_instance=self.org_1_instance_1, end_instance=self.org_1_instance_8)
        best_path = (100, [])
        if not paths.empty():
            best_path = paths.get()
        self.assertEqual(best_path[0], 100, best_path[1])

        paths = KnowledgeBaseUtils.get_instances_paths(start_instance=self.org_1_instance_0, end_instance=self.org_1_instance_4)
        best_path = (100, [])
        if not paths.empty():
            best_path = paths.get()
        self.assertEqual(best_path[0], 2, best_path[1])

    def test_get_related_instances(self):
        results = KnowledgeBaseUtils.get_related_instances(root_instance=self.org_1_instance_1, predicate_ids=None, level=2)
        self.assertEqual(len(results), 2, results)
        self.assertEqual(len(results[0]), 3, results)

        KnowledgeBaseUtils.get_related_instances(root_instance=self.org_1_instance_1, predicate_ids=None, level=10)
        self.assertEqual(len(results[0]), 3, results)

        predicate_ids = []
        KnowledgeBaseUtils.get_related_instances(root_instance=self.org_1_instance_1, predicate_ids=predicate_ids, level=10)
        self.assertEqual(len(results[0]), 3, results)


    def test_ontology_from_dict(self, model, data=None):
        pass
 
    def test_ontology_to_dict(self, model):
        pass

    def test_instances_from_dict(self, model, data=None):
        pass

    def test_instances_to_dict(self, model):
        pass

    def test_get_url(self, object_type, id):
        pass

