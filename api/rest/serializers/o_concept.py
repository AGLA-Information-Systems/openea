from rest_framework import serializers
from ontology.models import OConcept



class OConceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = OConcept
        fields = '__all__'
        #fields = ['id', 'name', 'description', 'model', 'organisation']