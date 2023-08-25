from queue import PriorityQueue
from uuid import UUID

from django.db.models import Q

from ontology.models import OConcept, OInstance, OPredicate, ORelation, OSlot



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
            for x in results[level]:
                KnowledgeBaseUtils.get_related_instances_recusrsive(results=results, already_found=already_found, instance=x[1], predicates=predicates, level=level + 1, max_level=max_level)

