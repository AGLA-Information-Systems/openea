from rest_framework import serializers
from ontology.models import Organisation


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'
        #fields = ['id', 'name', 'description', 'organisation']