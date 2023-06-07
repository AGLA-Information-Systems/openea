from django import forms

from ontology.models import OConcept, OModel, OPredicate
from ontology.plugins import EXPORT_FORMAT_CHOICES, IMPORT_FORMAT_CHOICES
from organisation.constants import KNOWLEDGE_SET_CHOICES, TIME_SCHEDULE_CHOICES
from organisation.controllers.security import SecurityController


class ModelImportForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', '')
        super(ModelImportForm, self).__init__(*args, **kwargs)
        user_organisations = list(SecurityController.get_user_organisations(user))
        self.fields['model'] = forms.ModelChoiceField(
            queryset=OModel.objects.filter(repository__organisation__in=user_organisations))


    #model_id = forms.CharField(max_length=100, required=True)
    knowledge_set = forms.ChoiceField(choices=KNOWLEDGE_SET_CHOICES, widget=forms.RadioSelect)
    import_file = forms.FileField(required=True)
    format = forms.ChoiceField(choices=IMPORT_FORMAT_CHOICES, widget=forms.Select)
    time_schedule = forms.ChoiceField(choices=TIME_SCHEDULE_CHOICES, widget=forms.RadioSelect)


class ModelExportForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', '')
        super(ModelExportForm, self).__init__(*args, **kwargs)
        user_organisations = list(SecurityController.get_user_organisations(user))
        self.fields['model'] = forms.ModelChoiceField(
            queryset=OModel.objects.filter(repository__organisation__in=user_organisations))

    #model_id = forms.CharField(max_length=100, required=True)
    knowledge_set = forms.ChoiceField(choices=KNOWLEDGE_SET_CHOICES, widget=forms.RadioSelect)
    format = forms.ChoiceField(choices=EXPORT_FORMAT_CHOICES, widget=forms.Select)
    time_schedule = forms.ChoiceField(choices=TIME_SCHEDULE_CHOICES, widget=forms.RadioSelect)


class ModelReportForm(forms.Form):
    model = forms.ModelChoiceField(queryset=OModel.objects.all())
    profit_predicate = forms.ModelChoiceField(queryset=OPredicate.objects.filter(model__id=1))
    cost_predicate = forms.ModelChoiceField(queryset=OPredicate.objects.filter(model__id=1))
    amount_concept = forms.ModelChoiceField(queryset=OConcept.objects.filter(model__id=1))


    def __init__(self, *args, **kwargs):
        initial_arguments = kwargs.pop('initial', {})
        user = kwargs.pop('user', '')
        super(ModelReportForm, self).__init__(*args, **kwargs)
        #user_organisations = list(SecurityController.get_user_organisations(user))
        #self.fields['model'] = forms.ModelChoiceField(
        #    queryset=OModel.objects.filter(repository__organisation__in=user_organisations))
        
        model_id = initial_arguments.get('model_id')
        model = OModel.objects.get(id=model_id)
        self.fields['model'].initial = model.id
        self.fields['amount_concept'].queryset=OConcept.objects.filter(model=model)
        self.fields['amount_concept'].initial = initial_arguments.get('amount_concept')
        self.fields['profit_predicate'].queryset=OPredicate.objects.filter(model=model)
        self.fields['profit_predicate'].initial = initial_arguments.get('profit_predicate')
        self.fields['cost_predicate'].queryset=OPredicate.objects.filter(model=model)
        self.fields['cost_predicate'].initial = initial_arguments.get('cost_predicate')