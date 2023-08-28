from django.core.exceptions import ObjectDoesNotExist

from ..models import OConcept, OModel, OPredicate, ORelation, Repository
from ..utils import get_index


BASIC_ONTOLOGY = {
    'entities': [
        [None, 'THING', 'The original subject of all entities'],
        [None, 'CLASS', "A class of THING"],
        [None, 'SLOT', "A property or aspect of a class"],
        [None, 'FACET', "A restriction on a slot"],
        [None, 'RELATION', "A predicate description"],
    ],
    'relations': [
        [None, 'is-a-subtype-of', "Relation describing the subsumption"],
        [None, 'is-classified-as', "Relation describing the instance of a class"],
        [None, 'is-part-of', "Relation describing the aggreagation"],
        [None, 'is-an-aspect-of', "Relation describing the ascpect/property of an concept"],
        [None, 'is-qualified-as', "Relation describing the instance of a class"],
        [None, 'is-equal-to', "Relation describing the equality of concepts"],
        [None, 'is-a-restriction-on', "Relation describing a restriction on an concept"]
    ],
    'ontology': [
        [None, None, 'CLASS', None, 'is-a-subtype-of', None, 'THING', ''],
        [None, None, 'SLOT', None, 'is-a-subtype-of', None, 'THING', ''],
        [None, None, 'FACET', None, 'is-a-subtype-of', None, 'THING', ''],
        [None, None, 'RELATION', None, 'is-a-subtype-of', None, 'THING', ''],       
        [None, None, 'SLOT', None, 'is-an-aspect-of', None, 'CLASS', ''],
        [None, None, 'FACET', None, 'is-a-restriction-on', None, 'SLOT', '']
    ]
}


EXAMPLE_ONTOLOGY = {
    'entities': [
        [None, 'mammal', 'group of vertebrate animals constituting the class Mammalia'],
        [None, 'human', 'group of vertebrate animals constituting the class Hominidae'],
        [None, 'color', 'visual perception of the frequency of light'],
        [None, 'hair-color', 'color of the hair'],
        [None, 'height', 'measurement from base to top'],
        [None, 'meter', 'unit of measurement of distance']
    ],
    'relations': [],
    'ontology': [
        [None, None, 'human', None, 'is-a-subtype-of', None, 'mammal', ''],
        [None, None, 'mammal', None, 'is-a-subtype-of', None, 'THING', ''],
        [None, None, 'color', None, 'is-a-subtype-of', None, 'THING', ''],
        [None, None, 'hair-color', None, 'is-a-subtype-of', None, 'THING', ''],      
        [None, None, 'hair-color', None, 'is-an-aspect-of', None, 'human', ''],
        [None, None, 'meter', None, 'is-a-subtype-of', None, 'THING', ''],
        [None, None, 'height', None, 'is-a-subtype-of', None, 'THING', ''],
        [None, None, 'height', None, 'is-an-aspect-of', None, 'human', '']
    ]
}


EXAMPLE_INSTANCES = {
    'instances': [
        [None, 'Kossi', '', None, 'human', None, 'hair-color', None, None, 'grey', '', None, 'color'],
        [None, 'Tom', '', None, 'human', None, 'hair-color', None, None, 'blonde', '', None, 'color'],
        [None, 'Jerry', '', None, 'human', None, 'hair-color', None, None, 'black', '', None, 'color'],
        [None, 'Jerry', '', None, 'human', None, 'height', None, None, '1.87', '', None, 'meter'],
    ]
}

DEFAULT_MAX_LEVEL=1000000

class KnowledgeBaseController:

    #======================================================================================
    # Repository

    def create_repository(name, description=''):
        try:
            repo = KnowledgeBaseController.get_repository(name=name)
        except:
            repo = Repository.objects.create(name=name, description=description)
            repo.save()
        return repo
    
    def get_repository(name, id=None):
        if id:
            try:
                return Repository.objects.get(id=id)
            except ObjectDoesNotExist:
                pass
        try:
            return Repository.objects.get(name=name)
        except:
            raise ValueError("MISSING_ENTITY:{}".format(name))
    
    #======================================================================================
    # Model

    def create_model(repository, name, description='', version='1.0'):
        try:
            model = KnowledgeBaseController.get_model(repository=repository, name=name, version=version)
        except:
            model = OModel.objects.create(repository=repository, name=name, description=description, version=version)
            model.save()
        return model
    
    def get_model(repository=None, name='', version='1.0', id=None):
        if id:
            try:
                return OModel.objects.get(id=id)
            except ObjectDoesNotExist:
                pass
        try:
            return OModel.objects.get(repository=repository, name=name, version=version)
        except:
            raise ValueError("MISSING_ENTITY:{}".format(name))
    
    #======================================================================================
    # Entities

    def create_concept(model, name, description=''):
        try:
            concept = OConcept.objects.create(model=model, name=name, description=description)
            concept.save()
            #print(name)
            return concept
        except:
            raise ValueError("UNEXPECTED:{}".format(name))

    def get_entities(model, name):
        return OConcept.objects.filter(model=model, name=name).all()

    def get_entities_in_model(model):
        return OConcept.objects.filter(model=model).all()

    def get_concept(model, name, class_name=None, id=None):
        if id:
            try:
                return OConcept.objects.get(id=id)
            except ObjectDoesNotExist:
                pass

        entities = KnowledgeBaseController.get_entities(model, name)
        if len(entities) == 1:
            return entities[0]

        if class_name:
            for concept in entities:
                classes = KnowledgeBaseController.get_linked_entities(results=[], level=0, concept=concept, predicate_name='is-classified-as', direction='object', max_level=1)
                for classe in classes:
                    if classe and classe.name == class_name:
                        return concept

                classes = KnowledgeBaseController.get_linked_entities(results=[], level=0, concept=concept, predicate_name='is-a-subtype-of', direction='object')
                for classe in classes:
                    if classe.name == class_name:
                        return concept
        raise ValueError("MISSING_ENTITY:{}".format(name))

    def get_leveled_linked_entities(results, level, concept, predicate_name, direction='object', max_level=DEFAULT_MAX_LEVEL):
        return KnowledgeBaseController.get_linked_entities_recursive(results=results, level=level, concept=concept, predicate_name=predicate_name, direction=direction, max_level=max_level)

    def get_linked_entities(results, level, concept, predicate_name, direction='object', max_level=DEFAULT_MAX_LEVEL):
        return get_index(KnowledgeBaseController.get_linked_entities_recursive(results=results, level=level, concept=concept, predicate_name=predicate_name, direction=direction, max_level=max_level))

    def get_linked_entities_recursive(results, level, concept, predicate_name, direction='object', max_level=DEFAULT_MAX_LEVEL):
        if level > max_level:
            return results

        level = level + 1
        direct_results = []
        
        if direction == 'subject':
            direct_links = concept.is_object_of.filter(relation__name=predicate_name).all()
        else:
            direct_links = concept.is_subject_of.filter(relation__name=predicate_name).all()
        
        for predicate in direct_links:
            if direction == 'subject':
                next_concept = predicate.subject
            else:
                next_concept = predicate.object
            if next_concept:
                results.append((next_concept, level))
            KnowledgeBaseController.get_linked_entities_recursive(results=results, level=level, concept=next_concept, predicate_name=predicate_name, direction=direction, max_level=max_level)
        
        return results

    #======================================================================================
    # Relations

    def create_relation(model, name, description=''):
        try:
            relation = ORelation.objects.get(model=model, name=name)
        except ObjectDoesNotExist:
            relation = ORelation.objects.create(relation=name, name=name, description=description)
            relation.save()
        return relation

    def get_relation(model, name, id=None):
        if id:
            try:
                return ORelation.objects.get(id=id)
            except ObjectDoesNotExist:
                pass
        try:
            return ORelation.objects.get(model=model, name=name)
        except:
            raise ValueError("MISSING_RELATION_TYPE:{}".format(name))

    #======================================================================================
    # Predicates

    def create_predicate(model, relation, subject, object, description=''):
        if isinstance(relation, str):
            relation = KnowledgeBaseController.get_relation(model=model, name=relation)

        try:
            return OPredicate.objects.get(model=model, relation=relation, subject=subject, object=object)
        except ObjectDoesNotExist:
            predicate = OPredicate.objects.create(model=model, subject=subject, relation=relation, object=object, description=description)
            predicate.save()
        return predicate

    def get_predicate(model, relation, subject, object, id=None):
        if id:
            try:
                return OPredicate.objects.get(id=id)
            except ObjectDoesNotExist:
                pass

        if isinstance(relation, str):
            relation = KnowledgeBaseController.get_relation(model=model, name=relation)

        try:
            return OPredicate.objects.get(model=model, relation=relation, subject=subject, object=object)
        except:
            raise ValueError("MISSING_PREDICATE:{} {} {}".format(subject, relation.name, object))

    #======================================================================================
    # Classes

    def get_classes_in_model(model):
        entities = KnowledgeBaseController.get_entities_in_model(model=model)
        for concept in entities:
            if concept.is_subject_of.filter(relation__name='is-classified-as').count() == 0:
                yield concept

    def get_class(model, name, id=None):
        if id:
            try:
                return OConcept.objects.get(id=id)
            except ObjectDoesNotExist:
                pass
        entities = KnowledgeBaseController.get_entities(model=model, name=name)
        classes = []
        for concept in entities:
            if concept.is_subject_of.filter(relation__name='is-classified-as').count() == 0:
                classes.append(concept)
        if len(classes) == 0:
            raise ValueError("MISSING_CLASS:{}".format(name))
        if len(classes) > 1:
            raise ValueError("DUPLICATE_CLASS:{}".format(name))
        return classes[0]

    def get_kinds(model, class_concept=None):
        return KnowledgeBaseController.get_linked_entities(results=[], level=0, concept=class_concept, predicate_name='is-a-subtype-of', direction='object')

    def get_conceptes(model, instance=None):
        classes = [x.object for x in instance.is_subject_of.filter(relation__name='is-classified-as').all()]
        if len(classes) == 0:
            return [KnowledgeBaseController.get_class(model=model, name='THING')]
        return classes
        
    
    #======================================================================================
    # Instances

    def get_instances_in_model(model):
        entities = KnowledgeBaseController.get_entities_in_model(model=model)
        for concept in entities:
            classes = [x.object for x in concept.is_subject_of.filter(relation__name='is-classified-as').all()]
            if len(classes) > 0:
                yield (concept, classes[0])

    def get_all_instances(model, name):
        entities = KnowledgeBaseController.get_entities(model=model, name=name)
        for concept in entities:
            if concept.is_subject_of.filter(relation__name='is-classified-as').count() > 0:
                yield concept

    def create_instance(model, name, concept, description=''):
        instance = KnowledgeBaseController.create_concept(model=model, name=name, description=description)
        KnowledgeBaseController.create_predicate(model=model, relation='is-classified-as', subject=instance, object=concept)
        return instance
    
    def get_instance(model, name, concept, id=None):
        if id:
            try:
                return OConcept.objects.get(id=id)
            except ObjectDoesNotExist:
                pass

        # for rel in concept.is_object_of.filter(relation__name='is-classified-as').all():
        #     print(rel.subject)

        for instance in KnowledgeBaseController.get_instances_recursive(model=model, concept=concept):
            if instance.name == name:
                return instance
        raise ValueError("MISSING_ENTITY:{}".format(name))

    def get_instances_recursive(model, concept, max_level=1):
        return KnowledgeBaseController.get_linked_entities(results=[], level=0, concept=concept, predicate_name='is-classified-as', direction='subject', max_level=max_level)
    
    #======================================================================================
    # Slot Templates

    def get_slot_templates(model, class_concept):
        kinds = KnowledgeBaseController.get_kinds(model, class_concept)
        slot_templates = [(class_concept, [x.subject for x in class_concept.is_object_of.filter(relation__name='is-an-aspect-of').all()])]
        for kind in kinds:
            slot_templates.append((kind, [x for x in KnowledgeBaseController.get_linked_entities(results=[], level=0, concept=kind, predicate_name='is-an-aspect-of', direction='subject', max_level=1) if x.is_subject_of.filter(relation__name='is-classified-as').count() == 0]))
        return slot_templates
        
    def get_slot_template(model, slot_name, id=None):
        if id:
            try:
                return OConcept.objects.get(id=id)
            except ObjectDoesNotExist:
                pass
        return KnowledgeBaseController.get_class(model=model, name=slot_name)

    #======================================================================================
    # Slots

    def create_slot(model, slot_name, slot_description, instance, concept):
        try:
            return KnowledgeBaseController.get_slot(model=model, slot_name=slot_name, instance=instance, concept=concept)
        except:
            pass

        slot_template = KnowledgeBaseController.get_slot_template(model=model, slot_name=slot_name)

        slot = OConcept.objects.create(model=model, name=slot_name, description=slot_description)
        slot.save()
        KnowledgeBaseController.create_predicate(model=model, relation='is-classified-as', subject=slot, object=slot_template)
        KnowledgeBaseController.create_predicate(model=model, relation='is-an-aspect-of', subject=slot, object=instance)
        return slot

    def get_slot(model, slot_name, instance, concept, id=None):
        if id:
            try:
                return OConcept.objects.get(id=id)
            except ObjectDoesNotExist:
                pass
        for slot in KnowledgeBaseController.get_slots(instance, concept):
            if slot.name == slot_name and slot.is_subject_of.filter(relation__name='is-classified-as').count() != 0:
                return slot
        raise ValueError("MISSING_ENTITY:{}".format(slot_name))
    
    def get_slots(model, instance, concept=None):
        for rel in instance.is_object_of.filter(relation__name='is-an-aspect-of').all():
            yield rel.subject

    #======================================================================================
    # Slots values

    def get_slot_value(model, slot, value_name, value_class=None, id=None):
        if id:
            try:
                return OConcept.objects.get(id=id)
            except ObjectDoesNotExist:
                pass
        for rel in KnowledgeBaseController.get_slot_values(model=model, slot=slot):
            if rel.object.name == value_name:
                return rel.object
        raise ValueError("MISSING_ENTITY:{}".format(value_name))

    def create_slot_value(model, slot, value_name, value_class, value_description):
        if model == None or slot == None or value_name == None or value_class == None:
            raise ValueError("INVALID_PARAMETERS:{}".format(locals()))
        value = KnowledgeBaseController.create_instance(model=model, name=value_name, description=value_description, concept=value_class)
        KnowledgeBaseController.create_predicate(model=model, relation='is-qualified-as', subject=slot, object=value)
        return value

    def set_slot_value(model, slot, slot_value):
        if slot == None or slot_value == None:
            raise ValueError("MISSING_ENTITY:{}".format('slots/slot_value'))
        return KnowledgeBaseController.create_predicate(model=model, relation='is-qualified-as', subject=slot, object=slot_value)

    def get_slot_values(model, slot):
        return slot.is_object_of.filter(relation__name='is-qualified-as').all()

    #======================================================================================
    # Facets

    def create_facet(model, slot, facet_name, facet_description):
        if model == None or slot == None or facet_name == None:
            raise ValueError("INVALID_PARAMETERS:{}".format([]))

        facet = KnowledgeBaseController.create_concept(model=model, name=facet_name, description=facet_description)
        KnowledgeBaseController.create_predicate(model=model, relation='is-a-restriction-on', subject=facet, object=slot)
        return facet

    def get_facet(model, slot, facet_name):
        if model == None or slot == None or facet_name == None:
            raise ValueError("INVALID_PARAMETERS:")

        return KnowledgeBaseController.get_concept(model=model, name=facet_name)


    def delete_facet(model, slot, facet_name):
        raise NotImplementedError

    #======================================================================================
    # Importer/Exporter

    def ontology_from_dict(model, data=BASIC_ONTOLOGY):
        for concept_def in data['entities']:
            print('id=',concept_def[0],',','name=',concept_def[1],',','description=',concept_def[2])
            try:
                concept = KnowledgeBaseController.get_class(model=model, name=concept_def[1], id=concept_def[0])
                concept.description = concept_def[2]
            except ValueError:
                concept = OConcept.objects.create(model=model, name=concept_def[1], description=concept_def[2])
            concept.save()

        for relation_def in data['relations']:
            print('id=',relation_def[0],',','name=',relation_def[1],',','description=',relation_def[2])
            try: 
                relation = KnowledgeBaseController.get_relation(model=model, name=relation_def[1], id=relation_def[0])
                relation.description = relation_def[2]
            except ValueError:
                relation = ORelation.objects.create(model=model, name=relation_def[1], description=relation_def[2])
            relation.save()


        for ontology in data['ontology']:
            predicate_id = ontology[0]
            subject_id = ontology[1]
            subject_name = ontology[2]
            relation_id = ontology[3]
            relation_name = ontology[4]
            object_id = ontology[5]
            object_name = ontology[6]
            predicate_description=ontology[7]

            print(
                'predicate_id=',predicate_id,',',
                'subject_id=',subject_id,',','subject_name=',subject_name,',',
                'relation_id=',relation_id,',','relation_name=',relation_name,',',
                'object_id=',object_id,',','object_name=',object_name)
            
            subject_concept = KnowledgeBaseController.get_class(model=model, name=subject_name, id=subject_id)
            relation = KnowledgeBaseController.get_relation(model=model, name=relation_name, id=relation_id)
            object_concept = KnowledgeBaseController.get_class(model=model, name=object_name, id=object_id)

            try:
                predicate = KnowledgeBaseController.get_predicate(model=model, subject=subject_concept, relation=relation, object=object_concept, id=predicate_id)
            except ValueError:
                predicate = KnowledgeBaseController.create_predicate(model=model, subject=subject_concept, relation=relation, object=object_concept, description=predicate_description)


    def ontology_to_dict(model):
        data = {
            'entities': [],
            'relations': [],
            'ontology': []
        }
        for concept in OConcept.objects.filter(model=model).all():
            data['entities'].append((concept.id, concept.name, concept.description))
        for relation in ORelation.objects.filter(model=model).all():
            data['relations'].append((relation.id, relation.name, relation.description))
        for predicate in OPredicate.objects.filter(model=model).all():
            data['ontology'].append(
               [predicate.id,
                predicate.subject.id,
                predicate.subject.name,
                predicate.relation.id,
                predicate.relation.name,
                predicate.object.id,
                predicate.object.name,
                predicate.description]
            )
        return data

    def instances_from_dict(model, data=EXAMPLE_INSTANCES):
        
        for instance_def in data['instances']:
            instance_id = instance_def[0]
            instance_name = instance_def[1]
            instance_description=instance_def[2]
            concept_id=instance_def[3]
            concept_name=instance_def[4]
            slot_id=instance_def[5]
            slot_name=instance_def[6]
            slot_class_id=instance_def[7]
            slot_value_id=instance_def[8]
            slot_value_name=instance_def[9]
            slot_value_description=instance_def[10]
            slot_value_class_id=instance_def[11]
            slot_value_class_name=instance_def[12]

            print(
            'instance_id=',instance_id,',','instance_name=',instance_name,',','instance_description=',instance_description,',',
            'concept_id=',concept_id,',','concept_name=',concept_name,','
            'slot_id=',slot_id,',','slot_name=',slot_name,',','slot_class_id=',slot_class_id,',',
            'slot_value_id=',slot_value_id,',','slot_value_name=',slot_value_name,',','slot_value_description=',slot_value_description,',',
            'slot_value_class_id=',instance_def[8],',','slot_value_class_name=',instance_def[9])

            concept = KnowledgeBaseController.get_class(model=model, name=concept_name, id=concept_id)
            slot_class = KnowledgeBaseController.get_class(model=model, name=slot_name, id=slot_class_id)
            slot_value_class = KnowledgeBaseController.get_class(model=model, name=slot_value_class_name, id=slot_value_class_id)

            try:
                instance = KnowledgeBaseController.get_instance(model=model, name=instance_name, concept=concept, id=instance_def[0])
            except:
                instance = KnowledgeBaseController.create_instance(model=model, name=instance_name, description=instance_description, concept=concept)

            try:
                slot = KnowledgeBaseController.get_slot(model=model, slot_name=slot_name, instance=instance, concept=concept, id=slot_id)
            except:
                slot = KnowledgeBaseController.create_slot(model=model, slot_name=slot_name, slot_description='', instance=instance, concept=concept)

            try:
                slot_value = KnowledgeBaseController.get_slot_value(model=model, value_name=slot_value_name, value_class=slot_value_class, slot=slot, id=slot_value_id)
            except:
                slot_value = KnowledgeBaseController.create_slot_value(model=model, value_name=slot_value_name, value_class=slot_value_class, value_description=slot_value_description, slot=slot)


    def instances_to_dict(model):
        data = {'instances': []}
        for predicate in OPredicate.objects.filter(model=model, relation__name='is-classified-as').all():
            result = [None, None, None, None, None, None, None, None, None, None, None, None, None]
            instance = predicate.subject
            concept = predicate.object
            result[0] = instance.id
            result[1] = instance.name
            result[2] = instance.description
            result[3] = concept.id
            result[4] = concept.name

            for slot in [x.subject for x in instance.is_object_of.filter(model=model, relation__name='is-an-aspect-of').all()]:
                result[5] = slot.id
                result[6] = slot.name

                slot_class = KnowledgeBaseController.get_class(model=model, name=slot.name)
                result[7] = slot_class.id

                slot_values = [y.object for y in slot.is_subject_of.filter(model=model, relation__name='is-qualified-as').all()]
                if len(slot_values) == 0:
                    data['instances'].append(list(result))
                    continue

                for slot_value in slot_values:
                    result[8] = slot_value.id
                    result[9] = slot_value.name
                    result[10] = slot_value.description

                    slot_value_classes = [z.object for z in slot_value.is_subject_of.filter(relation__name='is-classified-as').all()]
                    for slot_value_class in slot_value_classes:
                        result[11] = slot_value_class.id
                        result[12] = slot_value_class.name
                        data['instances'].append(list(result))
        return data
