import json, os
from django.conf import settings
from django.views.generic import DetailView
from django.http import JsonResponse
from django.http import HttpResponse
from django.core import serializers
import lxml.etree as ET
from authorization.controllers.utils import CustomPermissionRequiredMixin 
from django.contrib.auth.mixins import LoginRequiredMixin, create_organisation_admin_security_group
from django.contrib.auth.mixins import LoginRequiredMixin


from ontology.controllers.knowledge_base import KnowledgeBaseController
from ontology.models import OModel, OConcept, ORelation, OPredicate



class OModelReportView(LoginRequiredMixin, CustomPermissionRequiredMixin, DetailView):
    model = OModel
    #template_name = "o_model/o_model_report.xml"
    paginate_by = 10000
    #content_type = 'application/xml'
    permission_required = [('VIEW', model.get_object_type(), None)]


    def get_context_data(self, **kwargs):
        context = super(OModelReportView, self).get_context_data(**kwargs)
        
        context['entities'] = serializers.serialize('json', OConcept.objects.filter(model=context.get('object')).order_by('-created_at').all())
        context['relations'] = serializers.serialize('json', ORelation.objects.filter(model=context.get('object')).order_by('-created_at').all())
        context['predicates'] = serializers.serialize('json', OPredicate.objects.filter(model=context.get('object')).order_by('-created_at').all())

        return context
        
    """A base view for displaying a single object."""
    def get(self, request, *args, **kwargs):
        self.content_type = 'text/xml'
        self.object = self.get_object()
        
        # serialized_stores = serializers.serialize('xml',store_list)
        # return HttpResponse(serialized_stores, content_type='application/xml')

        dom = ET.parse(os.path.join(settings.BASE_DIR, './webapp/templates/report/reportXML.xml'))
        xslt = ET.parse(os.path.join(settings.BASE_DIR, './webapp/templates/report/application/core_al_app_cap_summary_custom.xsl'))
        transform = ET.XSLT(xslt)
        newdom = transform(dom)
        print(ET.tostring(newdom, pretty_print=True))
        response = HttpResponse(ET.tostring(newdom, pretty_print=True), content_type='text/xml')

        # xsl = libxslt.parseStyleSheetDoc(libxml2.parseFile('webapp/templates/report/application/core_al_app_cap_list_by_name.xsl'))
        # with open('webapp/templates/report/reportXML.xml') as f:
        #     contents = f.read()
        #     print(contents)
        # data = contents
        # result = xsl.applyStylesheet(data)
        # response = HttpResponse(ET.tostring(newdom, pretty_print=True), content_type='text/xml')
        # xsl.saveResultToFile(response, result)
        return response

        # self.object = self.get_object()
        # self.content_type = 'text/json'

        # data = {}
        # data.update(KnowledgeBaseController.ontology_to_dict(self.object))
        # data.update(KnowledgeBaseController.instances_to_dict(self.object))
        
        # # if self.request.GET:
        # #     data__ = JsonForm(request.GET)
        # #     if data__.is_valid():
        # #         json = data__.cleaned_data['json']
        # #         if json == 'true':
        # #             return JsonResponse({'data': data})
        # return JsonResponse({'data': data}, json_dumps_params={'ensure_ascii': False})
        # #return self.render_to_response(data)
