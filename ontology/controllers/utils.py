from queue import PriorityQueue
from uuid import UUID

from django.db.models import Q

from ontology.models import OConcept, OInstance, OPredicate, ORelation, OSlot

__author__ = "Patrick Agbokou"
__copyright__ = "Copyright 2021, OpenEA"
__credits__ = ["Patrick Agbokou"]
__license__ = "Apache License 2.0"
__version__ = "1.0.0"
__maintainer__ = "Patrick Agbokou"
__email__ = "patrick.agbokou@aglaglobal.com"
__status__ = "Development"

DEFAULT_MAX_LEVEL = 100


class KnowledgeBaseUtils:

    def get_parent_concepts(concept, max_level=DEFAULT_MAX_LEVEL):
        return KnowledgeBaseUtils.get_recursive_parent_concepts(concept, results=[], level=0, max_level=max_level)

    def get_recursive_parent_concepts(concept, results, level, max_level=DEFAULT_MAX_LEVEL):
        if level > max_level:
            return results
        parents = [x.subject for x in OPredicate.objects.filter(object=concept, relation__type=ORelation.INHERITANCE_SUPER_IS_SUBJECT)] + [
            x.object for x in OPredicate.objects.filter(subject=concept, relation__type=ORelation.INHERITANCE_SUPER_IS_OBJECT)]
        for x in parents:
            results = results + KnowledgeBaseUtils.get_recursive_parent_concepts(
                concept=x, results=results, level=level+1, max_level=DEFAULT_MAX_LEVEL)
        return [(x, level) for x in parents] + results

    def get_child_concepts(concept, max_level=DEFAULT_MAX_LEVEL):
        return KnowledgeBaseUtils.get_recursive_child_concepts(concept, results=[], level=0, max_level=max_level)

    def get_recursive_child_concepts(concept, results, level, max_level=DEFAULT_MAX_LEVEL):
        if level > max_level:
            return results
        children = [x.subject for x in OPredicate.objects.filter(object=concept, relation__type=ORelation.INHERITANCE_SUPER_IS_OBJECT)] + [
            x.object for x in OPredicate.objects.filter(subject=concept, relation__type=ORelation.INHERITANCE_SUPER_IS_SUBJECT)]
        for x in children:
            results = results + KnowledgeBaseUtils.get_recursive_child_concepts(
                concept=x, results=results, level=level+1, max_level=DEFAULT_MAX_LEVEL)
        return [(x, level) for x in children] + results

    def get_related_object_concepts(concept, predicate_ids, level=0, max_level=DEFAULT_MAX_LEVEL):
        predicates = OPredicate.objects.filter(subject=concept)
        if predicate_ids is not None and isinstance(predicate_ids, list):
            predicates = predicates.filter(id__in=predicate_ids)

        if level >= max_level:
            return [(x.object, level) for x in predicates]
        results = []
        for x in predicates:
            results = results + KnowledgeBaseUtils.get_related_object_concepts(
                level=level + 1, concept=x.object, predicate_ids=predicate_ids, max_level=max_level)
        return [(x.object, level) for x in predicates] + results

    def get_related_subject_concepts(concept, predicate_ids, level=0, max_level=DEFAULT_MAX_LEVEL):
        predicates = OPredicate.objects.filter(object=concept)
        if predicate_ids is not None and isinstance(predicate_ids, list):
            predicates = predicates.filter(id__in=predicate_ids)

        if level >= max_level:
            return [(x.subject, level) for x in predicates]
        results = []
        for x in predicates:
            results = results + KnowledgeBaseUtils.get_related_subject_concepts(
                level=level + 1, concept=x.subject, predicate_ids=predicate_ids, max_level=max_level)
        return [(x.subject, level) for x in predicates] + results


    def get_instances_paths(start_instance, end_instance):
        q = PriorityQueue(maxsize=5)
        path = []
        for x in OSlot.objects.filter((Q(subject=start_instance)|Q(object=start_instance))):
            new_path = list(path)
            new_path.append(x)
            KnowledgeBaseUtils.get_instances_path_recursive(slot=x, end_instance=end_instance, path=new_path, paths=q, level=0, max_level=DEFAULT_MAX_LEVEL)
        return q;


    def get_instances_path_recursive(slot, end_instance, path, paths, level=0, max_level=DEFAULT_MAX_LEVEL):
        if end_instance == slot.object or end_instance == slot.subject:
            paths.put((len(path), list(path)))
            return None
        
        if level >= max_level:
            return None
        
        for x in OSlot.objects.filter((Q(subject=slot.object)|Q(object=slot.subject)|Q(subject=slot.subject)|Q(object=slot.object))):
            if x not in path:
                new_path = list(path)
                new_path.append(x)
                KnowledgeBaseUtils.get_instances_path_recursive(slot=x, end_instance=end_instance, path=new_path, paths=paths, level=level + 1, max_level=max_level)
        
     
    def get_related_instances(root_instance, predicate_ids, level):
        results = {}
        already_found = []
        predicates = OPredicate.objects.filter(model=root_instance.model)
        if predicate_ids and isinstance(predicate_ids, list):
            predicates = predicates.filter(id__in=predicate_ids)
        
        results[0] = [(None, root_instance)]
        already_found = [root_instance]
        KnowledgeBaseUtils.get_related_instances_recusrsive(results=results, already_found=already_found, instance=root_instance, predicates=predicates, level=1, max_level=level)
        return results

    def get_related_instances_recusrsive(results, already_found, instance, predicates, level, max_level):
        if level >= max_level:
            return None
        found = [(x, x.object) for x in OSlot.objects.filter(subject=instance, predicate__in=predicates).all() if x.object not in already_found] + [(x, x.subject) for x in OSlot.objects.filter(object=instance, predicate__in=predicates).all() if x.subject not in already_found]
        if len(found) > 0:
            results[level] = found
            already_found = already_found + [x[1] for x in found]
            print(already_found)
            for x in results[level]:
                KnowledgeBaseUtils.get_related_instances_recusrsive(results=results, already_found=already_found, instance=x[1], predicates=predicates, level=level + 1, max_level=max_level)


    def ontology_from_dict(model, data=None):
        for concept_id, concept_data in data['concepts'].items():
            OConcept.get_or_create(
                id=concept_data['id'], model=model, name=concept_data['name'], description=concept_data['description'])
        for relation_id, relation_data in data['relations'].items():
            ORelation.get_or_create(
                id=concept_data['id'], model=model, name=relation_data['name'], description=relation_data['description'])
        for predicate_id, predicate_data in data['predicates'].items():
            subject = OConcept.objects.get(id=predicate_data['subject_id'])
            object = OConcept.objects.get(id=predicate_data['object_id'])
            relation = ORelation.objects.get(id=predicate_data['relation_id'])
            OPredicate.get_or_create(id=predicate_data['id'],  model=model, name=predicate_data['name'], description=predicate_data['description'], subject=subject,
                                     relation=relation, object=object, cardinality_min=predicate_data['cardinality_min'], cardinality_max=predicate_data['cardinality_max'])


    def ontology_to_dict(model):
        data = {
            'id': model.id,
            "type": "model",
            'name': model.name,
            "description": model.description,
            "concepts": {},
            "relations": {},
            "predicates": {},
            'url': KnowledgeBaseUtils.get_url('model', model.id)
            }
        for concept in OConcept.objects.filter(model=model).order_by('name'):
            parents = KnowledgeBaseUtils.get_parent_concepts(concept=concept)
            children = KnowledgeBaseUtils.get_child_concepts(concept=concept)
            data['concepts'][str(concept.id)] = {
                "id": concept.id,
                "name": concept.name,
                "description": concept.description,
                "parents": {str(x[0].id): x[0].name for x in parents},
                "children": {str(x[0].id): x[0].name for x in children},
                'url': KnowledgeBaseUtils.get_url('concept', concept.id)
            }
        for relation in ORelation.objects.filter(model=model).order_by('name'):
            data['relations'][str(relation.id)] = {
                "id": relation.id,
                "name": relation.name,
                "description": relation.description,
                "type": relation.type,
                'url': KnowledgeBaseUtils.get_url('relation', relation.id)
            }
        for predicate in OPredicate.objects.filter(model=model).order_by('subject__name').order_by('relation__name').order_by('object__name'):
            data['predicates'][str(predicate.id)] = {
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
        return data

    def instances_from_dict(model, data=None):
        # Create all instances
        for instance_id, instance_data in data['instances'].items():
            concept = OConcept.objects.get(id=instance_data['concept_id'])
            instance = OInstance.get_or_create(id=instance_data['id'],  model=model, name=instance_data['name'],
                                               code=instance_data['code'], description=instance_data['description'], concept=concept)
        # fill slots
        for instance_id, instance_data in data['instances'].items():
            instance = OInstance.objects.get(id=instance_id)
            for slot_id, slot in instance_data['ownslots'].items():
                object = OInstance.objects.get(id=slot['object_id'])
                predicate = OPredicate.objects.get(id=slot['predicate_id'])
                OSlot.get_or_create(id=slot_id, model=model, predicate=predicate,
                                    description=slot['description'], subject=instance, object=object)
            for slot_id, slot in instance_data['inslots'].items():
                subject = OInstance.objects.get(id=slot['subject_id'])
                predicate = OPredicate.objects.get(id=slot['predicate_id'])
                OSlot.get_or_create(id=slot_id, model=model, predicate=predicate,
                                    description=slot['description'], subject=subject, object=instance)

    def instances_to_dict(model, instance_ids=None):
        data = {
            'id': str(model.id),
            "type": "model",
            'name': model.name,
            "description": model.description,
            "predicates": {},
            "instances": {},
            'url': KnowledgeBaseUtils.get_url('model', model.id)
        }
        for predicate in OPredicate.objects.filter(model=model).all():
            data['predicates'][str(predicate.id)] = {
                "id": str(predicate.id),
                "subject_id": str(predicate.subject.id),
                "subject": predicate.subject.name,
                "relation_id": str(predicate.relation.id),
                "relation": predicate.relation.name,
                "object_id": str(predicate.object.id),
                "object": predicate.object.name,
                "cardinality_min": predicate.cardinality_min,
                "cardinality_max": predicate.cardinality_max,
                'url': KnowledgeBaseUtils.get_url('predicate', predicate.id)
            }

        if instance_ids:
            instances = OInstance.objects.filter(id__in=instance_ids).all()
        else:
            instances = OInstance.objects.filter(model=model).all()

        for instance in instances:
            data['instances'][str(instance.id)] = {
                "id": str(instance.id),
                "name": instance.name,
                'code': instance.code,
                "description": instance.description,
                "concept_id": str(instance.concept.id),
                "concept": instance.concept.name,
                "ownslots": {},
                "inslots": {},
                'url': KnowledgeBaseUtils.get_url('instance', instance.id)
            }
            for slot in OSlot.objects.filter(model=model, subject=instance).all():
                data['instances'][str(instance.id)]["ownslots"][str(slot.id)] = {
                    "id": str(slot.id),
                    "description": slot.description,
                    "predicate_id": str(slot.predicate.id),
                    "predicate": slot.predicate.name,
                    "relation_id": str(slot.predicate.relation.id),
                    "relation": slot.predicate.relation.name,
                    "concept_id": str(slot.predicate.object.id),
                    "concept": slot.predicate.object.name,
                    "object_id": str(slot.object.id) if slot.object is not None else None,
                    "object": slot.object.name if slot.object is not None else None,
                    "value": slot.value
                }
            for slot in OSlot.objects.filter(model=model, object=instance).all():
                data['instances'][str(instance.id)]["inslots"][str(slot.id)] = {
                    "id": str(slot.id),
                    "description": slot.description,
                    "predicate_id": str(slot.predicate.id),
                    "predicate": slot.predicate.name,
                    "relation_id": str(slot.predicate.relation.id),
                    "relation": slot.predicate.relation.name,
                    "concept_id": str(slot.predicate.subject.id),
                    "concept": slot.predicate.subject.name,
                    "subject_id": str(slot.subject.id),
                    "subject": slot.subject.name
                }
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
