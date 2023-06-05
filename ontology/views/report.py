from decimal import Decimal

from authorization.controllers.utils import CustomPermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from ontology.controllers.knowledge_base import KnowledgeBaseController
from ontology.controllers.utils import KnowledgeBaseUtils
from ontology.models import OInstance, OSlot

from django.shortcuts import render
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from ..forms import ModelReportForm


class ReportView(LoginRequiredMixin, CustomPermissionRequiredMixin, FormView):
    form_class = ModelReportForm
    template_name = 'model_report.html'
    success_url = reverse_lazy('model_report')
    
    def get(self, request, *args, **kwargs):
        #self.initial['model'] = kwargs.get('model_id')
        context = self.get_context_data(**kwargs)
        form = self.form_class(initial=context, user=self.request.user)
        context['form'] = form
        return self.render_to_response(context)
        

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form, **kwargs)
        else:
            return self.form_invalid(form, **kwargs)


    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        # here you can add things like:
        context['show_results'] = False
        return self.render_to_response(context)

    def form_valid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        # here you can add things like:
        model = form.cleaned_data.get('model')

        context['cost_predicate'] = form.cleaned_data.get('cost_predicate')
        context['profit_predicate'] = form.cleaned_data.get('profit_predicate')

        context['cost_concept'] = context['cost_predicate'].subject
        cost_concepts = [x[0] for x in KnowledgeBaseUtils.get_child_concepts(concept=context['cost_concept'])] + [context['cost_concept']]
        context['profit_concept'] = context['profit_predicate'].subject
        profit_concepts = [x[0] for x in KnowledgeBaseUtils.get_child_concepts(concept=context['profit_concept'])] + [context['profit_concept']]
        
        amount_concept = KnowledgeBaseController.get_class(model=model, name=form.cleaned_data.get('amount_concept'))       
        context['amount_concept'] = amount_concept
        if amount_concept != context['cost_predicate'].object or amount_concept != context['profit_predicate'].object:
            raise ValueError('The same concept of amount must be used')
        amount_concepts = [x[0] for x in KnowledgeBaseUtils.get_child_concepts(concept=amount_concept)] + [amount_concept]
        
        context['cost_instances'] = OInstance.objects.filter(model=model, concept__in=cost_concepts)
        context['cost_instances_amounts'] = {}
        for cost_instance in context['cost_instances']:
            context['cost_instances_amounts'][cost_instance.id] =  [x.object for x in OSlot.objects.filter(model=model, predicate=context['cost_predicate'], subject=cost_instance)] 
        context['profit_instances'] = OInstance.objects.filter(model=model, concept__in=profit_concepts)
        context['profit_instances_amounts'] = {}
        for profit_instance in context['profit_instances']:
            context['profit_instances_amounts'][profit_instance.id] = [x.object for x in OSlot.objects.filter(model=model, predicate=context['profit_predicate'], subject=profit_instance)] 

        
        
        context['summary'] = {}
        for instance_id, amounts in context['cost_instances_amounts'].items():
            for amount in amounts:
                if amount.concept not in context['summary']:
                    context['summary'][amount.concept] = {
                        'cost': 0,
                        'profit': 0,
                    }
                context['summary'][amount.concept]['cost'] = context['summary'][amount.concept]['cost'] + Decimal(amount.name) 
        for instance_id, amounts in context['profit_instances_amounts'].items():
            for amount in amounts:
                if amount.concept not in context['summary']:
                    context['summary'][amount.concept] = {
                        'cost': 0,
                        'profit': 0,
                    }
                context['summary'][amount.concept]['profit'] = context['summary'][amount.concept]['profit'] + Decimal(amount.name) 

        context['show_results'] = True
        
        return self.render_to_response(context)


    def get_initial(self):
        initials = super().get_initial()
        initials['model_id'] = self.kwargs.get('model_id')
        return initials

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context