from uuid import UUID

from django.db.models import Q

from authorization.controllers.utils import check_permission
from authorization.models import Permission
from ontology.controllers.utils import KnowledgeBaseUtils
from ontology.models import (OConcept, OInstance, OModel, OPredicate,
                             ORelation, OSlot)
from openea.utils import Utils

__author__ = "Patrick Agbokou"
__copyright__ = "Copyright 2021, OpenEA"
__credits__ = ["Patrick Agbokou"]
__license__ = "Apache License 2.0"
__version__ = "1.0.0"
__maintainer__ = "Patrick Agbokou"
__email__ = "patrick.agbokou@aglaglobal.com"
__status__ = "Development"

DEFAULT_MAX_LEVEL = 100

class ModelUtils:
    def filterSlots(user, data):
        return ModelUtils.filter(user, data)

    def filter(user, data):
        model_id = data.get('model_id')
        model = OModel.objects.get(id=model_id)
        target = data.get('target')

        relation_ids = ModelUtils.get_filtering_param(data, 'relation_ids', [])
        show_relations = check_permission(user=user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_RELATION)
        if not show_relations:
            relation_ids = []
        
            
        concept_ids = ModelUtils.get_filtering_param(data, 'concept_ids', [])
        show_concepts = check_permission(user=user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_CONCEPT)
        if not show_concepts:
            concept_ids = []
        
            
        predicate_ids = ModelUtils.get_filtering_param(data, 'predicate_ids', None)
        if not predicate_ids:
            predicate_ids = None
        show_predicates = check_permission(user=user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_PREDICATE)
        if not show_predicates:
            predicate_ids = []
        
            
        instance_ids = ModelUtils.get_filtering_param(data, 'instance_ids', None)
        if not instance_ids:
            instance_ids = None
        show_instances = check_permission(user=user, action=Permission.PERMISSION_ACTION_VIEW, object_type=Utils.OBJECT_INSTANCE)
        if not show_instances:
            instance_ids = []
        
            
        slot_ids = ModelUtils.get_filtering_param(data, 'slot_ids', None)
        if not show_instances:
            slot_ids = []
        
            

        filtered_data = {
            'relations': [],
            'concepts': [],
            'predicates': [],
            'instances': [],
            'slots': [],
        }

        filtered_data['relations'] = ORelation.objects.filter(model=model, id__in=relation_ids).order_by('name')
        if target == 'relations':
            return filtered_data

        filtered_data['concepts'] = OConcept.objects.filter(model=model, id__in=concept_ids).order_by('name')
        if target == 'concepts':
            return filtered_data

        filtered_data['predicates'] = OPredicate.objects.filter(model=model, relation__in=filtered_data['relations'], subject__in=filtered_data['concepts'], object__in=filtered_data['concepts']).order_by('subject__name').order_by('relation__name').order_by('object__name')
        if isinstance(predicate_ids, list):
            filtered_data['predicates'] = filtered_data['predicates'].filter(id__in=predicate_ids)
        if target == 'predicates':
            return filtered_data

        filtered_data['instances'] = OInstance.objects.filter(model=model, concept__in=filtered_data['concepts']).order_by('name')
        if filtered_data['predicates']:
            available_concept_ids = set([x.subject.id for x in filtered_data['predicates']] + [x.object.id for x in filtered_data['predicates']])
            filtered_data['instances'] = filtered_data['instances'].filter(concept_id__in=available_concept_ids)
        if isinstance(instance_ids, list):
            filtered_data['instances'] = filtered_data['instances'].filter(id__in=instance_ids)
        if target == 'instances':
            return filtered_data
        
        filtered_data['slots'] = OSlot.objects.filter((Q(subject__in=filtered_data['instances'])|Q(object__in=filtered_data['instances'])), model=model, predicate__in=filtered_data['predicates'])
        if isinstance(slot_ids, list):
            filtered_data['slots'] = filtered_data['slots'].filter(id__in=slot_ids)
        return filtered_data


    
    def model_from_dict():
        pass
    def concept_from_dict():
        pass
    def relation_from_dict():
        pass
    def predicate_from_dict():
        pass
    def instance_from_dict():
        pass
    def slot_from_dict():
        pass

    def model_to_dict(model):
        return {
            'id': model.id,
            "type": "model",
            'name': model.name,
            'version': model.version,
            "description": model.description,
            "concepts": {},
            "relations": {},
            "predicates": {},
            'url': KnowledgeBaseUtils.get_url('model', model.id)
        }
    
    def concept_to_dict(concept):
        return {
            "id": concept.id,
            "name": concept.name,
            "description": concept.description,
            'url': KnowledgeBaseUtils.get_url('concept', concept.id)
        }
    def relation_to_dict(relation):
        return {
            "id": relation.id,
            "name": relation.name,
            "description": relation.description,
            "type": relation.type,
            'url': KnowledgeBaseUtils.get_url('relation', relation.id)
        }
    def predicate_to_dict(predicate):
        return {
            "id": predicate.id,
            "subject_id": predicate.subject.id,
            "subject": predicate.subject.name,
            "relation_id": predicate.relation.id,
            "relation": predicate.relation.name,
            "object_id": predicate.object.id,
            "object": predicate.object.name,
            "cardinality_min": predicate.cardinality_min,
            "cardinality_max": predicate.cardinality_max,
            'url': KnowledgeBaseUtils.get_url('predicate', predicate.id)
        }
    
    def instance_to_dict(instance):
        data = {
            "id": instance.id,
            "name": instance.name,
            'code': instance.code,
            "description": instance.description,
            "concept_id": instance.concept.id,
            "concept": instance.concept.name,
            "ownslots": {},
            "inslots": {},
            'url': KnowledgeBaseUtils.get_url('instance', instance.id)
        }
        for slot in OSlot.objects.filter(subject=instance).all():
            data["ownslots"][str(slot.id)] = {
                "id": slot.id,
                "description": slot.description,
                "predicate_id": slot.predicate.id,
                "predicate": slot.predicate.name,
                "relation_id": slot.predicate.relation.id,
                "relation": slot.predicate.relation.name,
                "concept_id": slot.predicate.object.id,
                "concept": slot.predicate.object.name,
                "object_id": slot.object.id if slot.object is not None else None,
                "object": slot.object.name if slot.object is not None else None,
                "value": slot.value
            }
        for slot in OSlot.objects.filter(object=instance).all():
            data["inslots"][str(slot.id)] = {
                "id": slot.id,
                "description": slot.description,
                "predicate_id": slot.predicate.id,
                "predicate": slot.predicate.name,
                "relation_id": slot.predicate.relation.id,
                "relation": slot.predicate.relation.name,
                "concept_id": slot.predicate.subject.id,
                "concept": slot.predicate.subject.name,
                "subject_id": slot.subject.id,
                "subject": slot.subject.name
            }
        return data
    
    def slot_to_dict(slot):
        return {
            "id": slot.id,
            "description": slot.description,
            "predicate_id": slot.predicate.id,
            "predicate": slot.predicate.name,
            "relation_id": slot.predicate.relation.id,
            "relation": slot.predicate.relation.name,
            "concept_id": slot.predicate.object.id,
            "concept": slot.predicate.object.name,
            "subject_id": slot.subject.id,
            "subject": slot.subject.name,
            "object_id": slot.object.id if slot.object is not None else None,
            "object": slot.object.name if slot.object is not None else None,
            "value": slot.value
        }
    
    def get_filtering_param(data, key, default=None):
        value = data.get(key, default)
        if value and not isinstance(value, list):
            value = [value]
        return value
    

    def version_uuid(uuid):
        try:
            UUID(uuid).version
            return uuid
        except ValueError:
            return None
        

    def find_paths(start_instance, end_instance):
        paths = []
        q = KnowledgeBaseUtils.get_instances_paths(start_instance=start_instance, end_instance=end_instance)
        while not q.empty():
            best_path = q.get()
            paths.append([ModelUtils.slot_to_dict(x) for x in best_path[1]])
        return paths
    
    def analyze_impact(root_instance, predicate_ids, level):
        return KnowledgeBaseUtils.get_related_instances(root_instance, predicate_ids, level)
    
    def dictify_impact_analysis(results):
        dictified_results = {}
        for level, instances in results.items():
            dictified_results[level] = []
            for x in instances:
                slot_data = None
                if x[0]:
                    slot_data = ModelUtils.slot_to_dict(x[0])
                dictified_results[level].append((slot_data, ModelUtils.instance_to_dict(x[1])))
        return dictified_results
    
    def model_diff(model_1, model_2, filters):
        result = {
            'relations': [],
            'predicates': [],
            'concepts': [],
            'instances': [],
            'slots': [],
        }

        if 'relations' in filters:
            ModelUtils.compare(result, ORelation, 'relations', model_1, model_2)
        if 'predicates' in filters:
            ModelUtils.compare(result, OPredicate, 'predicates', model_1, model_2)
        if 'concepts' in filters:
            ModelUtils.compare(result, OConcept, 'concepts', model_1, model_2)
        if 'instances' in filters:
            ModelUtils.compare(result, OInstance, 'instances', model_1, model_2)
        if 'slots' in filters:
            ModelUtils.compare(result, OSlot, 'slots', model_1, model_2)

        return result

    def compare(result, class_name, key, model_1, model_2):
        if key == 'predicates':
            model_1_query = class_name.objects.filter(model=model_1).order_by('subject__name').order_by('relation__name').order_by('object__name')
            model_2_query = class_name.objects.filter(model=model_2).order_by('subject__name').order_by('relation__name').order_by('object__name')
        elif key == 'slots':
            model_1_query = class_name.objects.filter(model=model_1).order_by('subject__name').order_by('predicate__relation__name').order_by('object__name')
            model_2_query = class_name.objects.filter(model=model_2).order_by('subject__name').order_by('predicate__relation__name').order_by('object__name')
        else:
            model_1_query = class_name.objects.filter(model=model_1).order_by('name')
            model_2_query = class_name.objects.filter(model=model_2).order_by('name')

        model_1_item_list = [x for x in model_1_query.all()]
        model_2_item_list = [x for x in model_2_query.all()]
        is_model_1_larger_than_model_2 = len(model_1_item_list) > len(model_2_item_list)

        smaller_list = model_1_item_list
        larger_list = model_2_item_list
        if is_model_1_larger_than_model_2:
            smaller_list = model_2_item_list
            larger_list = model_1_item_list
        
        i = 0
        while i < len(larger_list):
            if i < len(smaller_list):
                ModelUtils.compare_objects(result, key, model_1_item_list[i], model_2_item_list[i])
            else:
                if is_model_1_larger_than_model_2:
                    result[key].append( (None, {"id": str(larger_list[i].id), "name": larger_list[i].name}) )
                else:
                    result[key].append( ({"id": str(larger_list[i].id), "name": larger_list[i].name}, None) )
            i = i + 1

        #tuples.sort(key=lambda x: x[0], reverse=True)
    
    def compare_objects(result, key, item_1, item_2):
        if item_1.name == item_2.name:
            result[key].append( ({"id": str(item_1.id), "name": item_1.name}, {"id": str(item_2.id), "name": item_2.name}) )
        else:
            if item_1.name < item_2.name:
                result[key].append( ({"id": str(item_1.id), "name": item_1.name}, None) )
            else:
                result[key].append( (None, {"id": str(item_2.id), "name": item_2.name}) )
