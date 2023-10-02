from rest_framework import serializers
from ontology.models import OSlot



class OSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = OSlot
        fields = '__all__'
        #fields = ['id', 'subject', 'predicate', 'object', 'name', 'description', 'value', 'model', 'organisation']