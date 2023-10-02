from rest_framework import serializers
from ontology.models import Repository


class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = '__all__'
        #fields = ['id', 'name', 'description', 'organisation']