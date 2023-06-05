import logging

from ontology.plugins.essential import EssentialPlugin
from ontology.plugins.excel import ExcelPlugin
from ontology.plugins.json import JSONPlugin
from ontology.plugins.plugin import ACTION_EXPORT, ACTION_IMPORT
from organisation.constants import KNOWLEDGE_SET_CHOICES

logger = logging.getLogger(__name__)

PLUGINS = [ExcelPlugin, JSONPlugin, EssentialPlugin]

IMPORT_PLUGINS = [x for x in PLUGINS if ACTION_IMPORT in x.available_actions()]
IMPORT_FORMAT_CHOICES = [x.get_format() for x in IMPORT_PLUGINS]
IMPORTERS = {(x.get_format()[0],y[0]):(getattr(x, "import_{}".format(y[0].lower())), x.get_file_extension(y[0])) for y in KNOWLEDGE_SET_CHOICES for x in IMPORT_PLUGINS}
logger.debug(IMPORTERS)

EXPORT_PLUGINS = [x for x in PLUGINS if ACTION_EXPORT in x.available_actions()]
EXPORT_FORMAT_CHOICES = [x.get_format() for x in EXPORT_PLUGINS]
EXPORTERS = {(x.get_format()[0],y[0]):(getattr(x, "export_{}".format(y[0].lower())), x.get_file_extension(y[0]))  for y in KNOWLEDGE_SET_CHOICES for x in EXPORT_PLUGINS}
logger.debug(EXPORTERS)
