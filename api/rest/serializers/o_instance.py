from rest_framework import serializers
from ontology.models import OInstance



class OInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OInstance
        fields = '__all__'
        #fields = ['id', 'name', 'description', 'model', 'organisation']