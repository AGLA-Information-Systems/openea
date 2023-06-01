from .controllers.knowledge_base_test import KnowledgeBaseControllerTestCase
from .o_concept import (OConceptCreateTestCase, OConceptDeleteTestCase,
                        OConceptDetailTestCase, OConceptListTestCase,
                        OConceptUpdateTestCase)
from .o_model import (OModelCreateTestCase, OModelDeleteTestCase,
                      OModelDetailTestCase, OModelListTestCase,
                      OModelUpdateTestCase)
from .o_predicate import (OPredicateCreateTestCase, OPredicateDeleteTestCase,
                          OPredicateDetailTestCase, OPredicateListTestCase,
                          OPredicateUpdateTestCase)
from .o_relation import (ORelationCreateTestCase, ORelationDeleteTestCase,
                         ORelationDetailTestCase, ORelationListTestCase,
                         ORelationUpdateTestCase)
from .o_slot import (OSlotCreateTestCase, OSlotDeleteTestCase,
                     OSlotDetailTestCase, OSlotListTestCase,
                     OSlotUpdateTestCase)
from .repository import (RepositoryCreateTestCase, RepositoryDeleteTestCase,
                         RepositoryDetailTestCase, RepositoryListTestCase,
                         RepositoryUpdateTestCase)
from .import_export import (ImportExportTestCase, ImportExportXMLTestCase)