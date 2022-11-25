from operator import mod
from ontology.models import OConcept, OInstance, OPredicate, ORelation, OSlot


DEFAULT_MAX_LEVEL = 100

class KnowledgeBaseUtils:

    def get_parent_concepts(concept, max_level=DEFAULT_MAX_LEVEL):
        return KnowledgeBaseUtils.get_recursive_parent_concepts(concept, results=[], level=0, max_level=max_level)

    def get_recursive_parent_concepts(concept, results, level, max_level=DEFAULT_MAX_LEVEL):
        if level > max_level:
            return results

        parents = [x.subject for x in OPredicate.objects.filter(object=concept, relation__type=ORelation.INHERITANCE_SUPER_IS_SUBJECT)] + [x.object for x in OPredicate.objects.filter(subject=concept, relation__type=ORelation.INHERITANCE_SUPER_IS_OBJECT)]
        results = results + [(x, level) for x in parents]
        for x in parents:
            KnowledgeBaseUtils.get_recursive_parent_concepts(concept=x, results=results, level=level+1, max_level=DEFAULT_MAX_LEVEL)
        return results  

    def get_child_concepts(concept, max_level=DEFAULT_MAX_LEVEL):
        return KnowledgeBaseUtils.get_recursive_child_concepts(concept, results=[], level=0, max_level=max_level)

    def get_recursive_child_concepts(concept, results, level, max_level=DEFAULT_MAX_LEVEL):
        if level > max_level:
            return results

        children = [x.subject for x in OPredicate.objects.filter(object=concept, relation__type=ORelation.INHERITANCE_SUPER_IS_OBJECT)] + [x.object for x in OPredicate.objects.filter(subject=concept, relation__type=ORelation.INHERITANCE_SUPER_IS_SUBJECT)]
        results = results + [(x, level) for x in children]
        for x in children:
            KnowledgeBaseUtils.get_recursive_child_concepts(concept=x, results=results, level=level+1, max_level=DEFAULT_MAX_LEVEL)
        return results  

    def get_leveled_linked_concepts(results, level, concept, relation_name, direction='object', max_level=DEFAULT_MAX_LEVEL):
        return KnowledgeBaseUtils.get_linked_concepts_recursive(results=results, level=level, concept=concept, relation_name=relation_name, direction=direction, max_level=max_level)

    def get_linked_concepts(results, level, concept, relation_name, direction='object', max_level=DEFAULT_MAX_LEVEL):
        return KnowledgeBaseUtils.get_linked_concepts_recursive(results=results, level=level, concept=concept, relation_name=relation_name, direction=direction, max_level=max_level)

    def get_linked_concepts_recursive(results, level, concept, relation_name, direction='object', max_level=DEFAULT_MAX_LEVEL):
        if level > max_level:
            return results

        level = level + 1
        direct_results = []
        
        if direction == 'subject':
            direct_links = concept.is_object_of.filter(relation__name=relation_name).all()
        else:
            direct_links = concept.is_subject_of.filter(relation__name=relation_name).all()
        
        for predicate in direct_links:
            if direction == 'subject':
                next_concept = predicate.subject
            else:
                next_concept = predicate.object
            if next_concept:
                results.append((next_concept, level))
            KnowledgeBaseUtils.get_linked_concepts_recursive(results=results, level=level, concept=next_concept, relation_name=relation_name, direction=direction, max_level=max_level)
        
        return results

    def ontology_from_dict(model, data=None):
        for concept_id, concept_data in data['concepts'].items():
            OConcept.get_or_create(id=concept_data['id'], model=model, name=concept_data['name'], description=concept_data['description'])
        for relation_id, relation_data in data['relations'].items():
            ORelation.get_or_create(id=concept_data['id'], model=model, name=relation_data['name'], description=relation_data['description'])
        for predicate_id, predicate_data in data['predicates'].items():
            subject = OConcept.objects.get(id=predicate_data['subject_id'])
            object = OConcept.objects.get(id=predicate_data['object_id'])
            relation = ORelation.objects.get(id=predicate_data['relation_id'])
            OPredicate.get_or_create(id=predicate_data['id'],  model=model, name=predicate_data['name'], description=predicate_data['description'], subject=subject, relation=relation, object=object, cardinality_min=predicate_data['cardinality_min'], cardinality_max=predicate_data['cardinality_max'])

 
    def ontology_to_dict(model):
        data = {
            'id': model.id,
            "type": "model",
            'name': model.name,
            "description": model.description,
            "concepts": {},
            "relations": {},
            "predicates": {}
            }
        for concept in OConcept.objects.filter(model=model).all():
            parents = KnowledgeBaseUtils.get_parent_concepts(concept=concept)
            children = KnowledgeBaseUtils.get_child_concepts(concept=concept)
            data['concepts'][str(concept.id)] = {
                "id": concept.id,
                "name": concept.name,
                "description": concept.description,
                "parents": {str(x[0].id): x[0].name for x in parents},
                "children": {str(x[0].id): x[0].name for x in children}
            }
        for relation in ORelation.objects.filter(model=model).all():
            data['relations'][str(relation.id)] = {
                "id": relation.id,
                "name": relation.name,
                "description": relation.description,
                "type": relation.type
            }
        for predicate in OPredicate.objects.filter(model=model).all():
            data['predicates'][str(predicate.id)] = {
                "id": predicate.id,
                "subject_id": predicate.subject.id,
                "subject": predicate.subject.name,
                "relation_id": predicate.relation.id,
                "relation": predicate.relation.name,
                "object_id": predicate.object.id,
                "object": predicate.object.name,
                "cardinality_min": predicate.cardinality_min,
                "cardinality_max": predicate.cardinality_max
            }
        return data

    def instances_from_dict(model, data=None):
        #Create all instances
        for instance_id, instance_data in data['instances'].items():
            concept = OConcept.objects.get(id=instance_data['concept_id'])
            instance = OInstance.get_or_create(id=instance_data['id'],  model=model, name=instance_data['name'], code=instance_data['code'], description=instance_data['description'], concept=concept)
        #fill slots
        for instance_id, instance_data in data['instances'].items():
            instance =  OInstance.objects.get(id=instance_id)
            for slot_id,slot in instance_data['ownslots'].items():
                object = OInstance.objects.get(id=slot['object_id'])
                predicate = OPredicate.objects.get(id=slot['predicate_id'])
                OSlot.get_or_create(id=slot_id, model=model, name=slot['name'], predicate=predicate, description=slot['description'], subject=instance, object=object)
            for slot_id,slot in instance_data['inslots'].items():
                subject = OInstance.objects.get(id=slot['subject_id'])
                predicate = OPredicate.objects.get(id=slot['predicate_id'])
                OSlot.get_or_create(id=slot_id, model=model, name=slot['name'], predicate=predicate, description=slot['description'], subject=subject, object=instance)



    def instances_to_dict(model):
        data = {
            'id': model.id,
            "type": "model",
            'name': model.name,
            "description": model.description,
            "predicates": {},
            "instances": {}
            }
        for predicate in OPredicate.objects.filter(model=model).all():
            data['predicates'][str(predicate.id)] = {
                "id": predicate.id,
                "subject_id": predicate.subject.id,
                "subject": predicate.subject.name,
                "relation_id": predicate.relation.id,
                "relation": predicate.relation.name,
                "object_id": predicate.object.id,
                "object": predicate.object.name,
                "cardinality_min": predicate.cardinality_min,
                "cardinality_max": predicate.cardinality_max
            }
        for instance in OInstance.objects.filter(model=model).all():
            data['instances'][str(instance.id)] = {
                "id": instance.id,
                "name": instance.name,
                'code': instance.code,
                "description": instance.description,
                "concept_id": instance.concept.id,
                "concept": instance.concept.name,
                "ownslots": {},
                "inslots": {}
            }
            for slot in OSlot.objects.filter(model=model, subject=instance).all():
                data['instances'][str(instance.id)]["ownslots"][str(slot.id)] = {
                    "id": slot.id,
                    "description": slot.description,
                    "predicate_id": slot.predicate.id,
                    "predicate": slot.predicate.name,
                    "relation_id": slot.predicate.relation.id,
                    "relation": slot.predicate.relation.name,
                    "concept_id": slot.object.concept.id,
                    "concept": slot.object.concept.name,
                    "object_id": slot.object.id,
                    "object": slot.object.name
                }
            for slot in OSlot.objects.filter(model=model, object=instance).all():
                data['instances'][str(instance.id)]["inslots"][str(slot.id)] = {
                    "id": slot.id,
                    "description": slot.description,
                    "predicate_id": slot.predicate.id,
                    "predicate": slot.predicate.name,
                    "relation_id": slot.predicate.relation.id,
                    "relation": slot.predicate.relation.name,
                    "concept_id": slot.subject.concept.id,
                    "concept": slot.subject.concept.name,
                    "subject_id": slot.subject.id,
                    "subject": slot.subject.name
                }
        return data
