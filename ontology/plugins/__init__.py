import inspect
import logging
import os
import sys

from ontology.plugins import *
from ontology.plugins.plugin import CAPABILITY_EXPORT, CAPABILITY_IMPORT, Plugin_v1
from organisation.constants import KNOWLEDGE_SET_CHOICES

logger = logging.getLogger(__name__)

PLUGINS = []

path = os.path.dirname(os.path.abspath(__file__))
# Dynamically load plugins
for py in [f[:-3] for f in os.listdir(path) if f.endswith('.py') and f != '__init__.py' and f != 'plugin.py']:
    mod = __import__('.'.join([__name__, py]), fromlist=[py])
    classes = [getattr(mod, x) for x in dir(mod) if isinstance(getattr(mod, x), type)]
    for cls in classes:
        setattr(sys.modules[__name__], cls.__name__, cls)
        if issubclass(cls, Plugin_v1) and cls != Plugin_v1:
            PLUGINS.append(cls)

IMPORT_PLUGINS = [x for x in PLUGINS if CAPABILITY_IMPORT in x.capabilities()]
IMPORT_FORMAT_CHOICES = [x.get_format() for x in IMPORT_PLUGINS]
IMPORTERS = {(x.get_format()[0],y[0]):(getattr(x, "import_{}".format(y[0].lower())), x.get_file_extension(y[0])) for y in KNOWLEDGE_SET_CHOICES for x in IMPORT_PLUGINS}
logger.debug(IMPORTERS)

EXPORT_PLUGINS = [x for x in PLUGINS if CAPABILITY_EXPORT in x.capabilities()]
EXPORT_FORMAT_CHOICES = [x.get_format() for x in EXPORT_PLUGINS]
EXPORTERS = {(x.get_format()[0],y[0]):(getattr(x, "export_{}".format(y[0].lower())), x.get_file_extension(y[0]))  for y in KNOWLEDGE_SET_CHOICES for x in EXPORT_PLUGINS}
logger.debug(EXPORTERS)
