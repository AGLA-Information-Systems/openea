from django import forms
from django_select2 import forms as s2forms
from django.utils.translation import gettext as _
from ontology.models import OModel
from taxonomy.models import Tag

class OModelCreateForm(forms.ModelForm):
    native_concepts = forms.BooleanField(label=_('With native concepts'), required=False)
    root_concept_name = forms.CharField(label=_('Root concept name (Leave blank for no root)'), required=False)

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial['native_concepts'] = True
        kwargs['initial'] = initial
        super(OModelCreateForm, self).__init__(*args, **kwargs)
    class Meta:
        model = OModel
        fields = ['name', 'version', 'description', 'repository',  'tags']
        widgets = {
            'tags': s2forms.ModelSelect2MultipleWidget(
                queryset=Tag.objects.all(),
                search_fields=['name__icontains']
            )
        }