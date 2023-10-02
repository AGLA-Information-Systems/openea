from rest_framework import serializers
from ontology.models import OModel



class OModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OModel
        fields = '__all__'
        #fields = ['id', 'name', 'version', 'description', 'repository', 'organisation']