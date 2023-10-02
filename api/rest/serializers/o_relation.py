from rest_framework import serializers
from ontology.models import ORelation



class ORelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ORelation
        fields = '__all__'
        #fields = ['id', 'name', 'description', 'model', 'organisation']