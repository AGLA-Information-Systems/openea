from rest_framework import serializers
from ontology.models import OPredicate



class OPredicateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OPredicate
        fields = '__all__'
        #fields = ['id', 'subject', 'relation', 'object', 'description', 'model', 'organisation']