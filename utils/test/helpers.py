from django.contrib.auth.models import User

from authorization.controllers.utils import DEFAULT_PERMISSIONS
from authorization.models import Permission, SecurityGroup
from ontology.models import (OConcept, OInstance, OModel, OPredicate,
                             ORelation, OReport, OSlot, Repository)
from organisation.models import Organisation, Profile, Task


def create_organisation(name='Org 1', description='', location='test'):
    org_1 = Organisation.objects.create(name=name, description=description, location=location)
    org_1.save()
    return org_1

def create_task(organisation, user, name='Org 1 Task 1', attachment=None, description='', type='', status='', config=''):
    org_1_task_1 = Task.objects.create(name=name, description=description, type=type, attachment=attachment, status=status, config=config, user=user, organisation=organisation)
    org_1_task_1.save()
    return org_1_task_1

def create_user(username='org1admin', password='12345'):
    org_1_admin_user = User.objects.create(username=username)
    org_1_admin_user.set_password(password)
    org_1_admin_user.save()
    return org_1_admin_user

def create_user_profile(organisation, user, role='Admin'):
    org_1_admin_profile = Profile.objects.create(role=role, user=user, organisation=organisation)
    org_1_admin_profile.save()
    return org_1_admin_profile

def create_security_group(organisation, name='Org 1 SecG', description=''):
    org_1_admin_security_group = SecurityGroup.objects.create(name=name, description=description, organisation=organisation)
    org_1_admin_security_group.save()
    return org_1_admin_security_group

def add_object_type_permissions_to_security_group(organisation, security_group, object_type):
    if security_group.organisation != organisation:
        raise ValueError("Security group does not belong to the organisation!")
    for action in DEFAULT_PERMISSIONS[object_type]:
        create_permission(security_group=security_group, action=action, object_type=object_type)

def create_permission(security_group, action, object_type):
    perm = Permission.get_or_create(action=action, object_type=object_type, organisation=security_group.organisation)
    perm.security_groups.add(security_group)
    perm.save()
    return perm

def create_repository(organisation, name='Org 1 Repo 1', description=''):
    org_1_repository = Repository.objects.create(name=name, description=description, organisation=organisation)
    org_1_repository.save()
    return org_1_repository

def create_model(repository, name='Org 1 Model 1', version='1.1', description=''):
    org_1_o_model = OModel.objects.create(name=name, version=version, description=description, repository=repository)
    org_1_o_model.save()
    return org_1_o_model

def create_report(model, name='Org 1 Report 1', path='/test', content='', description=''):
    org_1_o_report = OReport.objects.create(name=name, path=path, content=content, description=description, model=model)
    org_1_o_report.save()
    return org_1_o_report

def create_concept(model, name='Org 1 Concept 1', description=''):
    org_1_o_concept = OConcept.objects.create(name=name, description=description, model=model)
    org_1_o_concept.save()
    return org_1_o_concept

def create_relation(model, name='Org 1 Model 1', type=ORelation.PROPERTY, description=''):
    org_1_o_relation = ORelation.objects.create(name=name, type=type, description=description, model=model)
    org_1_o_relation.save()
    return org_1_o_relation

def create_predicate(model, subject, relation, object, description='', cardinality_min=0, cardinality_max=0):
    org_1_o_relation = OPredicate.objects.create(subject=subject, relation=relation, object=object, description=description, cardinality_min=cardinality_min, cardinality_max=cardinality_max, model=model)
    org_1_o_relation.save()
    return org_1_o_relation

def create_instance(model, concept, name='Org 1 Instance 1', description=''):
    org_1_o_instance = OInstance.objects.create(name=name, concept=concept, description=description, model=model)
    org_1_o_instance.save()
    return org_1_o_instance

def create_slot(model, subject, predicate, object, description=''):
    org_1_o_predicate = OSlot.objects.create(subject=subject, predicate=predicate, object=object, description=description, model=model)
    org_1_o_predicate.save()
    return org_1_o_predicate

def populate_test_env(x):
    x.org_1 = create_organisation(name='Org 1', description='', location='test')
    x.org_1_user_1 = create_user(username='org_1_user_1')
    x.org_1_user_1_profile = create_user_profile(role='Admin', user=x.org_1_user_1, organisation=x.org_1)
    x.org_1_security_group_1 = create_security_group(name='Org 1 SecG 1', description='', organisation=x.org_1)
    x.org_1_security_group_1.profiles.add(x.org_1_user_1_profile)
    x.object_type = OSlot.get_object_type()
    add_object_type_permissions_to_security_group(organisation=x.org_1, security_group=x.org_1_security_group_1, object_type=x.object_type)

    x.org_1_user_2 = create_user(username='org_1_user_2')
    x.org_1_user_2_profile = create_user_profile(role='Admin', user=x.org_1_user_2, organisation=x.org_1)
    x.org_1_security_group_2 = create_security_group(name='Org 1 SecG 2', description='', organisation=x.org_1)
    x.org_1_security_group_2.profiles.add(x.org_1_user_2_profile)

    x.org_1_repo_1 = create_repository(organisation=x.org_1, name='org_1_repo_1')
    x.org_1_model_1 = create_model(repository=x.org_1_repo_1, name='org_1_model_1')
    x.org_1_relation_1 = create_relation(model=x.org_1_model_1, name='org_1_relation_1')
    x.org_1_relation_2 = create_relation(model=x.org_1_model_1, name='org_1_relation_2', type=ORelation.INHERITANCE_SUPER_IS_OBJECT)
    x.org_1_relation_3 = create_relation(model=x.org_1_model_1, name='org_1_relation_3', type=ORelation.INHERITANCE_SUPER_IS_SUBJECT)

    # property
    x.org_1_concept_0 = create_concept(model=x.org_1_model_1, name='org_1_concept_0')
    x.org_1_concept_1 = create_concept(model=x.org_1_model_1, name='org_1_concept_1')
    x.org_1_concept_2 = create_concept(model=x.org_1_model_1, name='org_1_concept_2')
    x.org_1_predicate_1 = create_predicate(model=x.org_1_model_1, subject=x.org_1_concept_1, relation=x.org_1_relation_1, object=x.org_1_concept_2)

    # > has for parent >
    x.org_1_concept_3 = create_concept(model=x.org_1_model_1, name='org_1_concept_3')
    x.org_1_predicate_2 = create_predicate(model=x.org_1_model_1, subject=x.org_1_concept_2, relation=x.org_1_relation_2, object=x.org_1_concept_3)

    x.org_1_predicate_4 = create_predicate(model=x.org_1_model_1, subject=x.org_1_concept_1, relation=x.org_1_relation_2, object=x.org_1_concept_0)

    # > has for child >
    x.org_1_concept_4 = create_concept(model=x.org_1_model_1, name='org_1_concept_4')
    x.org_1_predicate_3 = create_predicate(model=x.org_1_model_1, subject=x.org_1_concept_1, relation=x.org_1_relation_3, object=x.org_1_concept_4)

    x.org_1_instance_0 = create_instance(model=x.org_1_model_1, concept=x.org_1_concept_0, name='org_1_instance_0')
    x.org_1_instance_1 = create_instance(model=x.org_1_model_1, concept=x.org_1_concept_1, name='org_1_instance_1')
    x.org_1_instance_2 = create_instance(model=x.org_1_model_1, concept=x.org_1_concept_2, name='org_1_instance_2')
    x.org_1_instance_3 = create_instance(model=x.org_1_model_1, concept=x.org_1_concept_3, name='org_1_instance_3')
    x.org_1_instance_4 = create_instance(model=x.org_1_model_1, concept=x.org_1_concept_4, name='org_1_instance_4')
    x.org_1_instance_5 = create_instance(model=x.org_1_model_1, concept=x.org_1_concept_1, name='org_1_instance_5')
    x.org_1_instance_6 = create_instance(model=x.org_1_model_1, concept=x.org_1_concept_2, name='org_1_instance_6')
    x.org_1_instance_7 = create_instance(model=x.org_1_model_1, concept=x.org_1_concept_3, name='org_1_instance_7')
    x.org_1_instance_8 = create_instance(model=x.org_1_model_1, concept=x.org_1_concept_4, name='org_1_instance_8')

    x.model_1_slot_1 = create_slot(model=x.org_1_model_1, subject=x.org_1_instance_1, predicate=x.org_1_predicate_1, object=x.org_1_instance_2)
    x.model_1_slot_2 = create_slot(model=x.org_1_model_1, subject=x.org_1_instance_2, predicate=x.org_1_predicate_2, object=x.org_1_instance_3)
    x.model_1_slot_3 = create_slot(model=x.org_1_model_1, subject=x.org_1_instance_1, predicate=x.org_1_predicate_3, object=x.org_1_instance_4)
    x.model_1_slot_4 = create_slot(model=x.org_1_model_1, subject=x.org_1_instance_1, predicate=x.org_1_predicate_4, object=x.org_1_instance_0)

    x.org_1_model_2 = create_model(repository=x.org_1_repo_1, name='org_1_model_2')
    
    return x

def populate_test_env_with_products():
    return populate_products()