from uuid import UUID

from django.db import transaction
from django.db.models import Q
from django.utils.translation import gettext as _

from authorization.models import Permission
from ontology.controllers.utils import KnowledgeBaseUtils
from ontology.models import (OConcept, OInstance, OModel, OPredicate,
                             ORelation, OReport, OSlot)
from openea.utils import Utils



DEFAULT_MAX_LEVEL = 100

class ModelUtils:
    def filterSlots(user, data):
        return ModelUtils.filter(user, data)

    def filter(user, data):
        model_id = data.get('model_id')
        model = OModel.objects.get(id=model_id)
        target = data.get('target')

        relation_ids = ModelUtils.get_filtering_param(data, 'relation_ids', [])
        show_relations = user.acl.check((Utils.PERMISSION_ACTION_VIEW, ORelation.get_object_type(), None))
        if not show_relations:
            relation_ids = []
        
            
        concept_ids = ModelUtils.get_filtering_param(data, 'concept_ids', [])
        show_concepts = user.acl.check((Utils.PERMISSION_ACTION_VIEW, OConcept.get_object_type(), None))
        if not show_concepts:
            concept_ids = []
        
            
        predicate_ids = ModelUtils.get_filtering_param(data, 'predicate_ids', None)
        if not predicate_ids:
            predicate_ids = None
        show_predicates = user.acl.check((Utils.PERMISSION_ACTION_VIEW, OPredicate.get_object_type(), None))
        if not show_predicates:
            predicate_ids = []
        
            
        instance_ids = ModelUtils.get_filtering_param(data, 'instance_ids', None)
        if not instance_ids:
            instance_ids = None
        show_instances = user.acl.check((Utils.PERMISSION_ACTION_VIEW, OInstance.get_object_type(), None))
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
            "instances": {},
            'url': ModelUtils.get_url('model', model.id)
        }
    
    def concept_to_dict(concept):
        return {
            "id": concept.id,
            "name": concept.name,
            "description": concept.description,
            'url': ModelUtils.get_url('concept', concept.id)
        }
    def relation_to_dict(relation):
        return {
            "id": relation.id,
            "name": relation.name,
            "description": relation.description,
            "type": relation.type,
            'url': ModelUtils.get_url('relation', relation.id)
        }
    def predicate_to_dict(predicate):
        return {
            "id": predicate.id,
            "description": predicate.description,
            "subject_id": predicate.subject.id,
            "subject": predicate.subject.name,
            "relation_id": predicate.relation.id,
            "relation": predicate.relation.name,
            "object_id": predicate.object.id,
            "object": predicate.object.name,
            "cardinality_min": predicate.cardinality_min,
            "cardinality_max": predicate.cardinality_max,
            'url': ModelUtils.get_url('predicate', predicate.id)
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
            'url': ModelUtils.get_url('instance', instance.id)
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
                "subject_id": slot.subject.id if slot.subject is not None else None,
                "subject": slot.subject.name if slot.subject is not None else None
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
            "subject_id": slot.subject.id if slot.subject is not None else None,
            "subject": slot.subject.name if slot.subject is not None else None,
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
                    if x[1] is not None:
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

    def model_copy(model):
        with transaction.atomic():
            old_model_id = model.id
            model_name = model.name + '_' + _('copy')
            new_model = OModel.objects.get(id=old_model_id)
            new_model.id = None
            new_model.name = model_name
            new_model.save()

            for relation in ORelation.objects.filter(model__id=old_model_id).order_by('name'):
                try:
                    ORelation.objects.get(model=new_model, name=relation.name)
                except ORelation.DoesNotExist:
                    new_relation = relation
                    new_relation.id = None
                    new_relation.model = new_model
                    new_relation.save()

            for concept in OConcept.objects.filter(model__id=old_model_id).order_by('name'):
                try:
                    OConcept.objects.get(model=new_model, name=concept.name)
                except OConcept.DoesNotExist:
                    new_concept = concept
                    new_concept.id = None
                    new_concept.model = new_model
                    new_concept.save()

            for instance in OInstance.objects.filter(model__id=old_model_id).order_by('name'):
                try:
                    OInstance.objects.get(model=new_model, name=instance.name, concept__name=instance.concept.name)
                except OInstance.DoesNotExist:
                    new_instance = instance
                    new_instance.id = None
                    new_instance.model = new_model
                    new_instance.concept = new_model.concepts.filter(name=instance.concept.name).first()
                    new_instance.save()
            
            for predicate in OPredicate.objects.filter(model__id=old_model_id).order_by('subject__name').order_by('relation__name').order_by('object__name'):
                try:
                    OPredicate.objects.get(model=new_model, subject__name=predicate.subject.name, relation__name=predicate.relation.name, object__name=predicate.object.name)
                except OPredicate.DoesNotExist:
                    new_predicate = predicate
                    new_predicate.id = None
                    new_predicate.model = new_model
                    new_predicate.subject = new_model.concepts.filter(name=predicate.subject.name).first()
                    new_predicate.relation = new_model.relations.filter(name=predicate.relation.name).first()
                    new_predicate.object = new_model.concepts.filter(name=predicate.object.name).first()
                    new_predicate.save()

            for slot in OSlot.objects.filter(model__id=old_model_id).order_by('subject__name').order_by('predicate__relation__name').order_by('object__name'):
                try:
                    slot_query = OSlot.objects.filter(model=new_model, predicate__relation__name=slot.predicate.relation.name)
                    if slot.subject:
                        slot_query = slot_query.filter(subject__name=slot.subject.name)
                    if slot.object:
                        slot_query = slot_query.filter(object__name=slot.object.name)
                    slot_query.get()
                except OSlot.DoesNotExist:
                    new_slot = OSlot.objects.get(id=slot.id)
                    new_slot.id = None
                    new_slot.model = new_model
                    new_slot.subject = None
                    if slot.subject:
                        new_slot.subject = new_model.model_instances.filter(name=slot.subject.name, concept__name=slot.subject.concept.name).first()
                    new_slot.predicate = new_model.predicates.filter(subject__name=slot.predicate.subject.name, relation__name=slot.predicate.relation.name, object__name=slot.predicate.object.name).first()
                    new_slot.object = None
                    if slot.object:
                        new_slot.object = new_model.model_instances.filter(name=slot.object.name, concept__name=slot.object.concept.name).first()
                    new_slot.save()

            for report in OReport.objects.filter(model__id=old_model_id).all():
                try:
                    OReport.objects.get(model=new_model, name=report.name)
                except OReport.DoesNotExist:
                    new_report = report
                    new_report.id = None
                    new_report.model = new_model
                    new_report.save()

        return new_model


    def model_delete():
        pass


    def ontology_from_dict(model, data=None, filters=None):
        concepts = data.get('concepts', {})
        if isinstance(concepts, list):
            concepts = {x['id']:x for x in concepts}
        for concept_id, concept_data in concepts.items():
            OConcept.get_or_create(
                id=concept_data['id'], 
                model=model, 
                name=concept_data['name'], 
                description=concept_data['description'])
            
        relations = data.get('relations', {})
        if isinstance(relations, list):
            relations = {x['id']:x for x in relations}
        for relation_id, relation_data in relations.items():
            ORelation.get_or_create(
                id=relation_data['id'], 
                model=model, 
                name=relation_data['name'],
                description=relation_data['description'])
            
        predicates = data.get('predicates', {})
        if isinstance(predicates, list):
            predicates = {x['id']:x for x in predicates}
        for predicate_id, predicate_data in predicates.items():
            subject = OConcept.objects.get(id=predicate_data['subject_id'])
            object = OConcept.objects.get(id=predicate_data['object_id'])
            relation = ORelation.objects.get(id=predicate_data['relation_id'])
            OPredicate.get_or_create(id=predicate_data['id'],
                                     model=model,
                                     description=predicate_data['description'],
                                     subject=subject,
                                     relation=relation,
                                     object=object, 
                                     cardinality_min=predicate_data['cardinality_min'],
                                     cardinality_max=predicate_data['cardinality_max'])


    def ontology_to_dict(model, filters=None, use_dicts=True, compute_inheritance=False):
        relation_ids = ModelUtils.get_filter(filters, 'relation_ids')
        concept_ids = ModelUtils.get_filter(filters, 'concept_ids')
        predicate_ids = ModelUtils.get_filter(filters, 'predicate_ids')

        data = ModelUtils.model_to_dict(model=model)
        
        if not use_dicts:
            data['concepts'] = []
            data['relations'] = []
            data['predicates'] = []

        concept_query = OConcept.objects.filter(model=model)
        if concept_ids:
            concept_query = concept_query.filter(id__in=concept_ids)
        for concept in concept_query.order_by('name'):
            concept_data = ModelUtils.concept_to_dict(concept=concept)
            if use_dicts:
                data['concepts'][str(concept.id)] = concept_data
            else:
                data['concepts'].append(concept_data)
            if compute_inheritance:
                parents = KnowledgeBaseUtils.get_parent_concepts(concept=concept)
                children = KnowledgeBaseUtils.get_child_concepts(concept=concept)
                concept_data['parents'] = [{str(x[0].id): x[0].name} for x in parents]
                concept_data['children'] = [{str(x[0].id): x[0].name} for x in children]
            
        relation_query = ORelation.objects.filter(model=model)
        if relation_ids:
            relation_query = relation_query.filter(id__in=relation_ids)
        for relation in relation_query.order_by('name'):
            relation_data = ModelUtils.relation_to_dict(relation=relation)
            if use_dicts:
                data['relations'][str(relation.id)] = relation_data
            else:
                data['relations'].append(relation_data)
        
        predicate_query = OPredicate.objects.filter(model=model)
        if predicate_ids:
            predicate_query = predicate_query.filter(id__in=predicate_ids)
        for predicate in predicate_query.order_by('subject__name').order_by('relation__name').order_by('object__name'):
            predicate_data = ModelUtils.predicate_to_dict(predicate=predicate)
            if use_dicts:
                data['predicates'][str(predicate.id)] = predicate_data
            else:
                data['predicates'].append(predicate_data)
        
        return data

    def instances_from_dict(model, data=None):
        instances = data.get('instances', {})
        if isinstance(instances, list):
            instances = {x['id']:x for x in instances}
        for instance_id, instance_data in instances.items():
            concept = OConcept.objects.get(id=instance_data['concept_id'])
            instance = OInstance.get_or_create(id=instance_data['id'],  model=model, name=instance_data['name'],
                                               code=instance_data['code'], description=instance_data['description'], concept=concept)
        # fill slots
        for instance_id, instance_data in data['instances'].items():
            instance = OInstance.objects.get(id=instance_id)
            for slot_id, slot in instance_data['ownslots'].items():
                object = OInstance.objects.get(id=slot['object_id'])
                predicate = OPredicate.objects.get(id=slot['predicate_id'])
                OSlot.get_or_create(id=slot_id,
                                    model=model,
                                    predicate=predicate,
                                    description=slot['description'],
                                    subject=instance,
                                    object=object)
            for slot_id, slot in instance_data['inslots'].items():
                subject = OInstance.objects.get(id=slot['subject_id'])
                predicate = OPredicate.objects.get(id=slot['predicate_id'])
                OSlot.get_or_create(id=slot_id,
                                    model=model,
                                    predicate=predicate,
                                    description=slot['description'],
                                    subject=subject,
                                    object=instance)

    def instances_to_dict(model, filters=None, use_dicts=True):
        
        predicate_ids = ModelUtils.get_filter(filters, 'predicate_ids')
        instance_ids = ModelUtils.get_filter(filters, 'instance_ids')

        data = ModelUtils.model_to_dict(model=model)

        if not use_dicts:
            data['predicates'] = []
            data['instances'] = []

        predicate_query = OPredicate.objects.filter(model=model)
        if predicate_ids:
            predicate_query = predicate_query.filter(id__in=predicate_ids)
        for predicate in predicate_query.order_by('subject__name').order_by('relation__name').order_by('object__name'):
            predicate_data = ModelUtils.predicate_to_dict(predicate=predicate)
            if use_dicts:
                data['predicates'][str(predicate.id)] = predicate_data
            else:
                data['predicates'].append(predicate_data)
                

        instance_query = OInstance.objects.filter(model=model)
        if instance_ids:
            instance_query = instance_query.filter(id__in=instance_ids)
        for instance in instance_query.order_by('name'):
            instance_data = ModelUtils.instance_to_dict(instance=instance)
            if use_dicts:
                data['instances'][str(instance.id)] = instance_data
            else:
                data['instances'].append(instance_data)

        return data

    def get_url(object_type, id):
        object_types = {
            'model': '/o_model/detail/',
            'concept': '/o_concept/detail/',
            'relation': '/o_relation/detail/',
            'predicate': '/o_predicate/detail/',
            'instance': '/o_instance/detail/'
        }
        return object_types[object_type] + str(id)


    def process_POST_array(post_data, variable_name):
        items = []
        for variable, value in post_data.items():
            if variable.startswith(variable_name):
                items.append(value)
        return items
    

    def get_filter(filters, item_name):
        item_ids = None
        if filters is not None and item_name in filters:
            item_ids = filters[item_name]
            if isinstance(item_ids, str):
                item_ids = [item_ids]
        return item_ids