
"""
{Description}
{License_info}
"""

import os

import xmltodict
from django.db import transaction

from ontology.controllers.o_model import ModelUtils
from ontology.plugins.plugin import CAPABILITY_EXPORT, CAPABILITY_IMPORT, Plugin_v1





class XMLPlugin(Plugin_v1):
    def capabilities():
        return {CAPABILITY_IMPORT, CAPABILITY_EXPORT}

    def get_format():
        return ('XML', 'XML')

    def get_file_extension(knowledge_set):
        return 'xml'

    def import_ontology(model, path, filename='ontology.xml', filters=None):
        with transaction.atomic():
            with open(os.path.join(path, filename), 'r') as f:
                data = xmltodict.parse(f.read())
                ModelUtils.ontology_from_dict(model, data=data['model'], filters=filters)

    def export_ontology(model, path, filename='ontology.xml', filters=None):
        with transaction.atomic():
            with open(os.path.join(path, filename), 'w') as f:
                data = ModelUtils.ontology_to_dict(model, filters=filters, use_dicts=False)
                f.write(xmltodict.unparse({'model':data}, pretty=True))

    def import_instances(model, path, filename='instances.xml', filters=None):
        with transaction.atomic():
            with open(os.path.join(path, filename), 'r') as f:
                data = xmltodict.parse(f.read())
                ModelUtils.instances_from_dict(model, data=data['model'], filters=filters)

    def export_instances(model, path, filename='instances.xml', filters=None):
        with transaction.atomic():
            with open(os.path.join(path, filename), 'w') as f:
                data = ModelUtils.instances_to_dict(model, filters=filters, use_dicts=False)
                f.write(xmltodict.unparse({'model':data}, pretty=True))
