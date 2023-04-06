from django import forms
from django_select2 import forms as s2forms

from ontology.models import OModel
from taxonomy.models import Tag

class OModelUpdateForm(forms.ModelForm):
    class Meta:
        model = OModel
        fields = ['name', 'version', 'description', 'repository',  'tags']
        widgets = {
            'tags': s2forms.ModelSelect2MultipleWidget(
                queryset=Tag.objects.all(),
                search_fields=['name__icontains']
            )
        }