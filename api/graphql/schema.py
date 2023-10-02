import graphene
from graphene_django import DjangoObjectType #used to change Django object into a format that is readable by GraphQL
from ontology.models import OConcept, OInstance, OModel, OPredicate, ORelation, Repository
from organisation.models import Organisation


class OrganisationType(DjangoObjectType):
    # Describe the data that is to be formatted into GraphQL fields
    class Meta:
        model = Organisation
        field = ("id", "name", "location", "description")

class RepositoryType(DjangoObjectType):
    # Describe the data that is to be formatted into GraphQL fields
    class Meta:
        model = Repository
        field = ("id", "name", "description", "organisation")

class OModelType(DjangoObjectType):
    # Describe the data that is to be formatted into GraphQL fields
    class Meta:
        model = OModel
        field = ("id", "name", "version", "description", "repository", "organisation")

class ORelationType(DjangoObjectType):
    # Describe the data that is to be formatted into GraphQL fields
    class Meta:
        model = ORelation
        field = ("id", "name", "description", "description", "model", "organisation")

class OConceptType(DjangoObjectType):
    # Describe the data that is to be formatted into GraphQL fields
    class Meta:
        model = OConcept
        field = ("id", "name", "version", "description", "model", "organisation")

class OPredicateType(DjangoObjectType):
    # Describe the data that is to be formatted into GraphQL fields
    class Meta:
        model = OPredicate
        field = ("id", "subject", "relation", "object", "description", "model", "organisation")

class OInstanceType(DjangoObjectType):
    # Describe the data that is to be formatted into GraphQL fields
    class Meta:
        model = OInstance
        field = ("id", "name", "version", "description", "concept", "model", "organisation")

class Query(graphene.ObjectType):
    o_organisation_list=graphene.List(OrganisationType)
    o_repository_list=graphene.List(RepositoryType)
    o_model_list=graphene.List(OModelType)
    o_model_detail_by_name = graphene.Field(OModelType, name=graphene.String(required=False), version=graphene.String(required=False))
    o_relation_list=graphene.List(ORelationType)
    o_concept_list=graphene.List(OConceptType)
    o_predicate_list=graphene.List(OPredicateType)
    o_instance_list=graphene.List(OInstanceType)

    def resolve_o_organisation_list(root, info, name=None, version=None):
        return Organisation.objects.all()
    
    def resolve_o_repository_list(root, info, name=None, version=None):
        return Repository.objects.all()
    
    def resolve_o_model_list(root, info, name=None, version=None):
        return OModel.objects.all()
    
    def resolve_o_model_detail_by_name(root, info, name, version=None):
        try:
            return OModel.objects.get(name=name, version=version)
        except OModel.DoesNotExist:
            return None
        
    def resolve_o_relation_list(root, info, name=None):
        return ORelation.objects.all()
    
    def resolve_o_relation_detail_by_name(root, info, name):
        try:
            return ORelation.objects.get(name=name)
        except ORelation.DoesNotExist:
            return None
    

    def resolve_o_concept_list(root, info, name=None):
        return OConcept.objects.all()
    
    def resolve_o_concept_detail_by_name(root, info, name):
        try:
            return OConcept.objects.get(name=name)
        except OConcept.DoesNotExist:
            return None
    

    def resolve_o_predicate_list(root, info, subject_name=None, relation_name=None, object_name=None):
        return OPredicate.objects.all()
    

    def resolve_o_instance_list(root, info, name=None, concept_name=None):
        return OInstance.objects.all()
    
    def resolve_o_instance_detail_by_name(root, info, name):
        try:
            return OInstance.objects.get(name=name)
        except OInstance.DoesNotExist:
            return None

schema = graphene.Schema(query=Query)