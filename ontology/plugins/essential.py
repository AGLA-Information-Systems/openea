
"""
{Description}
{License_info}
"""
import os
import re
import urllib.parse

from django.db import transaction

from ontology.controllers.knowledge_base import KnowledgeBaseController
from ontology.plugins.plugin import CAPABILITY_IMPORT, Plugin_v1
from organisation.constants import (KNOWLEDGE_SET_INSTANCES,
                                    KNOWLEDGE_SET_ONTOLOGY)

__author__ = "Patrick Agbokou"
__copyright__ = "Copyright 2021, OpenEA"
__credits__ = ["Patrick Agbokou"]
__license__ = "Apache License 2.0"
__version__ = "1.0.0"
__maintainer__ = "Patrick Agbokou"
__email__ = "patrick.agbokou@aglaglobal.com"
__status__ = "Development"


ESSENTIAL_ONTOLOGY = {
    'entities': [
        [None, ':THING', 'The original subject of all entities'],
        [None, ':SYSTEM-CLASS', "A system concept"],
        [None, ':ANNOTATION', "A note"],
        [None, ':INSTANCE-ANNOTATION', "A note"],
        [None, ':CONSTRAINT', "A constraint"],
        [None, ':PAL-CONSTRAINT', "A constraint"],
        [None, ':META-CLASS', "A note"],
        [None, ':CLASS', "A class of THING"],
        [None, ':SLOT', "A property or aspect of a class"],
        [None, ':FACET', "A restriction on a slot"],
        [None, ':STANDARD-CLASS', "A class of thing"],
        [None, ':STANDARD-SLOT', "A property or aspect of a class"],
        [None, ':STANDARD-FACET', "A restriction on a slot"],
        [None, ':RELATION', "A predicate description"],
        [None, ':DIRECTED-BINARY-RELATION', "A directed predicate"],

        [None, ':PAL-DESCRIPTION', "A directed predicate"],
        [None, ':PAL-NAME', "A directed predicate"],
        [None, ':PAL-RANGE', "A directed predicate"],
        [None, ':PAL-STATEMENT', "A directed predicate"],

        [None, ':ANNOTATION-TEXT', "A note"],
        [None, ':CREATION-TIMESTAMP', "the timestamp of creation of the file"],
        [None, ':CREATOR', "the user who created the file"],
        [None, ':ASSOCIATED-SLOT', "the slot associated to the facet"],
        [None, ':ASSOCIATED-FACET', "the facet associated to the slot"],
        [None, ':ESSENTIAL-SLOT', "the facet associated to the slot"],

        [None, 'name', "default property of a thing"],
        [None, 'description', "default property of a thing"]

    ],
    'relations': [
        [None, 'is-a-subtype-of', "Relation describing the subsumption"],
        [None, 'is-classified-as', "Relation describing the instance of a class"],
        [None, 'is-part-of', "Relation describing the aggreagation"],
        [None, 'is-an-aspect-of', "Relation describing the ascpect/property of an concept"],
        [None, 'is-equal-to', "Relation describing the equality of concepts"],
        [None, 'is-a-restriction-on', "Relation describing a restriction on an concept"],
        [None, 'is-qualified-as', "Relation describing the attribution of value"]
    ],
    'ontology': [
        [None, None, 'name', None, 'is-an-aspect-of', None, ':THING'],
        [None, None, 'description', None, 'is-an-aspect-of', None, ':THING'],

        [None, None, ':ANNOTATION', None, 'is-a-subtype-of', None, ':THING'],
        [None, None, ':INSTANCE-ANNOTATION', None, 'is-a-subtype-of', None, ':ANNOTATION'],
        [None, None, ':CONSTRAINT', None, 'is-a-subtype-of', None, ':THING'],
        [None, None, ':PAL-CONSTRAINT', None, 'is-a-subtype-of', None, ":CONSTRAINT"],
        [None, None, ':META-CLASS', None, 'is-a-subtype-of', None, ':THING'],
        [None, None, ':CLASS', None, 'is-a-subtype-of', None, ':META-CLASS'],
        [None, None, ':SLOT', None, 'is-a-subtype-of', None, ':META-CLASS'],
        [None, None, ':FACET', None, 'is-a-subtype-of', None, ':META-CLASS'],
        [None, None, ':STANDARD-CLASS', None, 'is-a-subtype-of', None, ':CLASS'],
        [None, None, ':STANDARD-SLOT', None, 'is-a-subtype-of', None, ':SLOT'],
        [None, None, ':STANDARD-FACET', None, 'is-a-subtype-of', None, ':FACET'],
        [None, None, ':DIRECTED-BINARY-RELATION', None, 'is-a-subtype-of', None, ':RELATION'],
        [None, None, ':SLOT', None, 'is-an-aspect-of', None, ':CLASS'],
        [None, None, ':FACET', None, 'is-a-restriction-on', None, ':SLOT'],

        [None, None, ':PAL-DESCRIPTION', None, 'is-an-aspect-of', None, ':PAL-CONSTRAINT'],
        [None, None, ':PAL-NAME', None, 'is-an-aspect-of', None, ':PAL-CONSTRAINT'],
        [None, None, ':PAL-RANGE', None, 'is-an-aspect-of', None, ':PAL-CONSTRAINT'],
        [None, None, ':PAL-STATEMENT', None, 'is-an-aspect-of', None, ':PAL-CONSTRAINT'],
        
        [None, None, ':ESSENTIAL-SLOT', None, 'is-a-subtype-of', None, ':STANDARD-SLOT'],
        [None, None, ':ANNOTATION-TEXT', None, 'is-an-aspect-of', None, ':INSTANCE-ANNOTATION'],
        [None, None, ':CREATION-TIMESTAMP', None, 'is-an-aspect-of', None, ':INSTANCE-ANNOTATION'],
        [None, None, ':CREATOR', None, 'is-an-aspect-of', None, ':INSTANCE-ANNOTATION'],
        [None, None, ':ASSOCIATED-SLOT', None, 'is-an-aspect-of', None, ':STANDARD-FACET'],
        [None, None, ':ASSOCIATED-FACET', None, 'is-an-aspect-of', None, ':ESSENTIAL-SLOT']
    ]
}


class EssentialPlugin(Plugin_v1):

    def capabilities():
        return {CAPABILITY_IMPORT}

    def get_format():
        return ('ESSENTIAL', 'Essential')

    def get_file_extension(knowledge_set):
        if knowledge_set == KNOWLEDGE_SET_ONTOLOGY:
            return 'pont'
        elif knowledge_set == KNOWLEDGE_SET_INSTANCES:
            return 'pins'

    def import_ontology(model, path, filename='import.pont'):
        with transaction.atomic():
            for block in EssentialPlugin.parse_file(path, filename):
                #print(block)
                data = EssentialPlugin.data_from_block(block)
                for datum in data:
                    if 'type' in datum:
                        EssentialPlugin.create_pont_concept(model=model, data=datum)

    def create_pont_concept(model, data):
        ret = {'slots': []}
        if data['type'] == 'defclass':
            ret['name'] = data['values'][0]
            ret['description'] = data['values'][1]
            for x in data['values'][2:]:
                try:
                    if 'type' in x and x['type'] == 'is-a':
                        ret['is-a'] = x['values'][0]
                    if 'type' in x and x['type'] == 'role':
                        ret['role'] = x['values'][0]
                    if 'type' in x and (x['type'] == 'single-slot' or x['type'] == 'multislot'):
                        slot = {'name': x['values'][0]}
                        for y in x['values'][1:]:
                            if 'type' in y and y['type'] == 'type':
                                slot['value_class'] = y['values'][0]
                            if 'type' in y and y['type'] == 'cardinality':
                                slot['cardinality'] = y['values']
                            if 'type' in y and y['type'] == 'allowed-classes':
                                slot['allowed-classes'] = y['values']
                            if 'type' in y and y['type'] == 'create-accessor':
                                slot['create-accessor'] = y['values'][0]
                            if 'type' in y and y['type'] == 'comment':
                                slot['description'] = y['values'][0]
                            
                        ret['slots'].append(slot)
                except:
                    print(x)
                    raise
        #print('==>', ret)
        
        if 'name' in ret:

            concept_class = None
            try:
                concept_class = KnowledgeBaseController.get_class(model=model, name=ret['name'])
            except ValueError:
                concept_class = KnowledgeBaseController.create_concept(model=model, name=ret['name'], description=ret.get('description'))

            slot_relation = KnowledgeBaseController.get_relation(model=model, name='is-an-aspect-of')
            slot_value_relation = KnowledgeBaseController.get_relation(model=model, name='is-qualified-as')
            facet_relation = KnowledgeBaseController.get_relation(model=model, name='is-a-restriction-on')

            for slot in ret['slots']:
                slot_class = None
                try:
                    try:
                        slot_class = KnowledgeBaseController.get_class(model=model, name=slot['name'])
                    except ValueError:
                        slot_class = KnowledgeBaseController.create_concept(model=model, name=slot['name'], description=slot.get('description'))
                    try:
                        slot_predicate = KnowledgeBaseController.get_predicate(model=model, relation=slot_relation, subject=slot_class, object=concept_class)
                    except ValueError:
                        slot_predicate = KnowledgeBaseController.create_predicate(model=model, relation=slot_relation, subject=slot_class, object=concept_class)

                    try:
                        slot_value_class = KnowledgeBaseController.get_class(model=model, name=slot['value_class'])
                    except ValueError:
                        slot_value_class = KnowledgeBaseController.create_concept(model=model, name=slot['value_class'], description='')
                    try:
                        slot_value_predicate = KnowledgeBaseController.get_predicate(model=model, relation=slot_value_relation, subject=slot_class, object=slot_value_class)
                    except ValueError:
                        slot_value_predicate = KnowledgeBaseController.create_predicate(model=model, relation=slot_value_relation, subject=slot_class, object=slot_value_class)

                    facet_classes = {}
                    for facet_name in ['cardinality', 'allowed-classes']:
                        if facet_name in slot:
                            facet_class = facet_classes.get(facet_name)
                            if facet_class is None:
                                try:
                                    facet_classes[facet_name] = KnowledgeBaseController.get_class(model=model, name=facet_name)
                                except ValueError:
                                    facet_classes[facet_name] = KnowledgeBaseController.create_concept(model=model, name=facet_name, description='')
                                facet_class = facet_classes[facet_name]
                            
                            try:
                                facet_instance = KnowledgeBaseController.get_instance(model=model, name=str(slot[facet_name]), concept=facet_class)
                            except ValueError:
                                facet_instance = KnowledgeBaseController.create_instance(model=model, name=str(slot[facet_name]), concept=facet_class)

                            try:
                                facet_predicate = KnowledgeBaseController.get_predicate(model=model, relation=facet_relation, subject=facet_instance, object=slot_class)
                            except ValueError:
                                facet_predicate = KnowledgeBaseController.create_predicate(model=model, relation=facet_relation, subject=facet_instance, object=slot_class)
                        
                except Exception as exc:
                    print(exc,' ', slot['name'])
                    raise

    def data_from_block(data):
        broken_data = data.replace('(', ' (').replace(')', ' ) ').replace('\\"', '').split(' ')
        current_object = {'type': 'root', 'values': []}
        object_stack = [current_object]
        long_string_mode = False
        tmp_w = []

        for w in list(filter(None, broken_data)):
            w = w.strip()

            if w.endswith('"'):
                long_string_mode = False
                w = w[:-1]
                tmp_w.append(w)
                w = ' '.join(tmp_w)
                tmp_w = []

            elif w.startswith('"'):
                long_string_mode = True
                w = w[1:]
            
            if long_string_mode == True:
                tmp_w.append(w)
                continue
            
            try:
                if w.startswith('('):
                    command = w[1:]
                    new_object = {'type': "{}".format(command), 'values': []}
                    object_stack.append(new_object)
                    current_object = new_object
                    #print('>>>>>>', current_object)
                    continue

                if w == ')':
                    new_object = object_stack.pop()
                    current_object = object_stack[-1]
                    current_object['values'].append(new_object)
                    #print('<<<<<<', new_object)
                    continue

            except IndexError:
                print('==== ', new_object)
                raise

            current_object['values'].append(w)

        return current_object['values']


    def import_instances(model, path, filename='import.pont'):
        with transaction.atomic():
            essential_refs = {'_____count':0}
            for block in EssentialPlugin.parse_file(path, filename):
                #print('===== Block ====>', block)
                data = EssentialPlugin.data_from_block(block)
                for datum in data:
                    if 'type' in datum:
                        #print('===== Datum ====>', datum)
                        EssentialPlugin.create_pins_concept(model=model, data=datum, essential_refs=essential_refs)
                        

    def create_pins_concept(model, data, essential_refs):
        ret = {'slots': []}
        ret['name'] = data['type']
        ret['display_name'] = None
        if 'values' in data and 'of' in data['values']:
            ret['predicate'] = data['values'][0]
            ret['class'] = data['values'][1]
            for x in data['values'][2:]:
                slot = {}
                if 'type' in x and x['type'] == 'name':
                    ret['display_name'] = x['values'][0]
                slot[x['type']] = x['values']
                ret['slots'].append(slot)
            # track essential internal references
            if 'display_name' in ret:
                if ret['name'] in essential_refs and essential_refs[ret['name']] != ret['display_name']:
                    ret['display_name'] = ret['display_name'] + essential_refs['_____count']
                    essential_refs['_____count'] = essential_refs['_____count'] + 1
                essential_refs[ret['name']] = ret['display_name']

            print('==>', ret)

            if 'class' in ret:
                concept = KnowledgeBaseController.get_class(model=model, name=ret['class'])

                try:
                    instance_name = essential_refs.get(ret['name']) or ret['name'][1:-1]
                    instance = KnowledgeBaseController.get_instance(model=model, name=instance_name, concept=concept)
                except ValueError:
                    instance = KnowledgeBaseController.create_instance(model=model, name=instance_name, concept=concept)

                relation = KnowledgeBaseController.get_relation(model=model, name='is-an-aspect-of')

                for slot in ret['slots']:
                    try:
                        if slot:
                            slot_name = list(slot.keys())[0]
                            slot_values = slot[slot_name]
                            if slot_name != 'name':
                                
                                slot_class = KnowledgeBaseController.get_class(model=model, name=slot_name)
                                
                                slot_value_class = KnowledgeBaseController.get_class(model=model, name=':THING')
                                slot_value_classes = [x.subject for x in slot_class.is_object_of.filter(relation__name='is-qualified-as').all()]
                                if len(slot_value_classes) > 0:
                                    slot_value_class = slot_value_classes[0]

                                try:
                                    slot_instance = KnowledgeBaseController.get_slot(model=model, slot_name=slot_name, instance=instance, concept=concept)
                                except ValueError:
                                    slot_instance = KnowledgeBaseController.create_slot(model=model, slot_name=slot_name, slot_description='', instance=instance, concept=concept)

                                for slot_value in slot_values:
                                    slot_value_name = slot_value
                                    if slot_value.startswith('[') and slot_value.endswith(']'):
                                        slot_value_name = essential_refs.get(slot_value) or slot_value[1:-1]
                                        slot_value = KnowledgeBaseController.get_instance(model=model, name=slot_value_name, )

                                    try:
                                        slot_value = KnowledgeBaseController.get_slot_value(model=model, value_name=slot_value_name, value_class=slot_value_class, slot=slot_instance)
                                    except:
                                        slot_value = KnowledgeBaseController.create_slot_value(model=model, value_name=slot_value_name, value_class=slot_value_class, value_description='', slot=slot_instance)

                                
                    except Exception as exc:
                        print(str(exc), ' ', slot)
                        raise

    def parse_file(path, filename='essential.p'):
        with open(os.path.join(path, filename), 'r') as f:
            parentheses = 0
            buffer = []
            object_count = 0
            line_count = 0
            for line in f:
                line_count = line_count + 1
                code_string = re.sub(r'".*?"', '""', line)

                parentheses += code_string.count('(')
                if parentheses > 0:
                    buffer.append(urllib.parse.unquote(line.replace('\n', '').replace('\t', '').replace(';+', ' ').replace(';', ' ')))
                parentheses -= code_string.count(')')

                if parentheses == 0 and buffer:
                    object_count = object_count + 1
                    block = ' '.join(buffer)
                    buffer = []
                    yield block
