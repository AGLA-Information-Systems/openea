import textwrap as tr

import graphviz
from django.conf import settings

from ontology.controllers.o_model import ModelUtils


class GraphvizController:
    
    def render_model_graph (format, model_data, knowledge_set='instances'):
        if not format:
            format = 'svg'

        model = model_data.get('model')

        dot = graphviz.Digraph( engine='fdp',
                                comment='OpenEA',
                                graph_attr={
                                    'id': 'modelgraph',
                                    'label': GraphvizController.get_graph_label(model),
                                    'splines': 'ortho',
                                    'sep': '1',
                                    'K': '0.5',
                                    #'overlap': 'compress',
                                    #'ranksep':'1',
                                    'fontname': 'arial',
                                    'fontsize': '12',
                                    'fontcolor': '#212529'},
                                node_attr={
                                    'shape': 'box',
                                    'style': 'filled,rounded',
                                    'maxTextWidth': '3.3',
                                    'fontname': 'arial',
                                    'fontsize': '12',
                                    'color': '#6c757d',
                                    'fontcolor': '#212529',
                                    'fillcolor': '#efefef'},
                                edge_attr={
                                    'fontname': 'arial',
                                    'fontsize': '12',
                                    'color': '#6c757d',
                                    'fontcolor': '#212529'})
        
        dot.splines = 'ortho'
        if knowledge_set == 'ontology':
            GraphvizController.render_ontology (dot, model_data['predicates'])
        elif knowledge_set == 'instances':
            GraphvizController.render_instances (dot, model_data['slots'])
        
        #dot_ = dot.unflatten(stagger=1)
        dot.format = format
        return dot.pipe(encoding='utf-8')

    def render_ontology (dot, predicates_data):
        nbr_edges = 0
        for predicate in predicates_data:
            dot.node(str(predicate.subject.id), label=GraphvizController.get_concept_label(predicate.subject), href=ModelUtils.get_url('concept', predicate.subject.id))
            dot.node(str(predicate.object.id), label=GraphvizController.get_concept_label(predicate.object), href=ModelUtils.get_url('concept', predicate.object.id))
            dot.edge(str(predicate.subject.id), str(predicate.object.id), label=GraphvizController.get_relation_label(predicate.relation), href=ModelUtils.get_url('predicate', predicate.id))
            if nbr_edges >= settings.MAX_GRAPH_NODES:
                break
            nbr_edges =+ 1

    def render_instances (dot, slots_data):
        nbr_edges = 0
        for slot in slots_data:
            if slot.subject is not None:
                dot.node(str(slot.subject.id), label=GraphvizController.get_instance_label(slot.subject), href=ModelUtils.get_url('instance', slot.subject.id))
            if slot.object is not None:
                dot.node(str(slot.object.id), label=GraphvizController.get_instance_label(slot.object), href=ModelUtils.get_url('instance', slot.object.id))
            if slot.subject is not None and slot.object is not None:
                dot.edge(str(slot.subject.id), str(slot.object.id), label=GraphvizController.get_predicate_label(slot.predicate), href=ModelUtils.get_url('predicate', slot.predicate.id))
            if nbr_edges >= settings.MAX_GRAPH_NODES:
                break
            nbr_edges =+ 1
    
    def wrap(s, default_size=settings.MAX_LENGTH_GRAPH_NODE_TEXT):
        return '\n'.join(tr.wrap(s, default_size))

    def get_graph_label(model):
        return 'OpenEA - © ' + model.organisation.name +' - ' + model.name + ' ' + model.version
    
    def get_relation_label(relation):
        return GraphvizController.wrap(relation.name)
    
    def get_concept_label(concept):
        return GraphvizController.wrap(concept.name)
    
    def get_predicate_label(predicate):
        return GraphvizController.wrap(predicate.name)

    def get_instance_label(instance):
        return  GraphvizController.wrap(instance.name) + '\n' + '(' + GraphvizController.wrap(instance.concept.name) + ')'


    def render_impact_analysis (format, data):
        if not format:
            format = 'svg'
        
        model = data.get('model')
        nodes = data.get('nodes')

        dot = graphviz.Digraph( engine='twopi',
                                comment='OpenEA',
                                graph_attr={
                                    'id': 'modelgraph',
                                    'label': GraphvizController.get_graph_label(model),
                                    'overlap': 'false',
                                    #'splines': 'curved',
                                    'ranksep':'2',
                                    'fontname': 'arial',
                                    'fontsize': '12',
                                    'fontcolor': '#212529'},
                                node_attr={
                                    'style':'filled',
                                    'maxTextWidth': '3.3',
                                    'fontname': 'arial',
                                    'fontsize': '12',
                                    'color': '#6c757d',
                                    'fontcolor': '#212529',
                                    'fillcolor': '#efefef'},
                                edge_attr={
                                    'fontname': 'arial',
                                    'fontsize': '12',
                                    'color': '#6c757d',
                                    'fontcolor': '#212529'})
        for level, x_list in nodes.items():
            GraphvizController.render_instances(dot=dot, slots_data=[x[0] for x in x_list if x[0]])
        dot.graph_attr['root'] = str(nodes[0][0][1].id)
    
        dot.format = format
        return dot.pipe(encoding='utf-8')
