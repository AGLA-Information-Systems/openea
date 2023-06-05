
"""
{Description}
{License_info}
"""
import json
import os
from uuid import UUID

from django.db import transaction

from ontology.controllers.o_model import ModelUtils
from ontology.plugins.plugin import ACTION_EXPORT, ACTION_IMPORT, Plugin

__author__ = "Patrick Agbokou"
__copyright__ = "Copyright 2021, OpenEA"
__credits__ = ["Patrick Agbokou"]
__license__ = "Apache License 2.0"
__version__ = "1.0.0"
__maintainer__ = "Patrick Agbokou"
__email__ = "patrick.agbokou@aglaglobal.com"
__status__ = "Development"


class GenericEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class JSONPlugin(Plugin):
    def available_actions():
        return {ACTION_IMPORT, ACTION_EXPORT}

    def get_format():
        return ('JSON', 'Json')

    def get_file_extension(knowledge_set):
        return 'json'

    def import_ontology(model, path, filename='ontology.json'):
        with transaction.atomic():
            with open(os.path.join(path, filename), 'r') as f:
                data = json.load(f)
                ModelUtils.ontology_from_dict(model, data=data)

    def export_ontology(model, path, filename='ontology.json', filters=None):
        with transaction.atomic():
            with open(os.path.join(path, filename), 'w') as f:
                json.dump(ModelUtils.ontology_to_dict(model, filters=filters), f, cls=GenericEncoder, ensure_ascii=False)

    def import_instances(model, path, filename='instances.json'):
        with transaction.atomic():
            with open(os.path.join(path, filename), 'r') as f:
                data = json.load(f)
                ModelUtils.instances_from_dict(model, data=data)

    def export_instances(model, path, filename='instances.json', filters=None):
        with transaction.atomic():
            with open(os.path.join(path, filename), 'w') as f:
                json.dump(ModelUtils.instances_to_dict(model, filters=filters), f, cls=GenericEncoder, ensure_ascii=False)
