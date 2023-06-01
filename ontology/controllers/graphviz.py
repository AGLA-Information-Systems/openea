import textwrap as tr

import graphviz
from django.conf import settings

from ontology.controllers.utils import KnowledgeBaseUtils


class GraphizController:
    
    def build (format, model_data, knowledge_set='instances'):
        if not format:
            format = 'svg'

        model = model_data.get('model')

        dot = graphviz.Digraph( engine='fdp',
                                comment='OpenEA',
                                graph_attr={
                                    'id': 'modelgraph',
                                    'label': 'OpenEA - '+ model.name + ' ' + model.version,
                                    'splines': 'ortho',
                                    'sep': '2',
                                    'ranksep':'2',
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
            GraphizController.render_ontology (dot, model_data['predicates'])
        elif knowledge_set == 'instances':
            GraphizController.render_instances (dot, model_data['slots'])
        
        dot_ = dot.unflatten(stagger=1)
        dot_.format = format
        return dot_.pipe(encoding='utf-8')

    def render_ontology (dot, predicates_data):
        nbr_nodes = 0
        for predicate in predicates_data:
            dot.node(str(predicate.subject.id), GraphizController.wrap(predicate.subject.name), href=KnowledgeBaseUtils.get_url('concept', predicate.subject.id))
            dot.node(str(predicate.object.id), GraphizController.wrap(predicate.object.name), href=KnowledgeBaseUtils.get_url('concept', predicate.object.id))
            dot.edge(str(predicate.subject.id), str(predicate.object.id), label=predicate.relation.name, constraint='false', href=KnowledgeBaseUtils.get_url('predicate', predicate.id))
            if nbr_nodes >= settings.MAX_GRAPH_NODES:
                break

    def render_instances (dot, slots_data):
        nbr_nodes = 0
        for slot in slots_data:
            dot.node(str(slot.subject.id), GraphizController.wrap(slot.subject.name), href=KnowledgeBaseUtils.get_url('instance', slot.subject.id))
            if slot.object is not None:
                dot.node(str(slot.object.id), GraphizController.wrap(slot.object.name), href=KnowledgeBaseUtils.get_url('instance', slot.object.id))
                dot.edge(str(slot.subject.id), str(slot.object.id), label=slot.predicate.relation.name, constraint='false', href=KnowledgeBaseUtils.get_url('predicate', slot.predicate.id))
            if nbr_nodes >= settings.MAX_GRAPH_NODES:
                break
    
    def wrap(s):
        return '\n'.join(tr.wrap(s, settings.MAX_LENGTH_GRAPH_NODE_TEXT))


    def render_impact_analysis (format, data):
        if not format:
            format = 'svg'
        
        model = data.get('model')
        nodes = data.get('nodes')

        dot = graphviz.Digraph( engine='twopi',
                                comment='OpenEA',
                                graph_attr={
                                    'id': 'modelgraph',
                                    'label': 'OpenEA - '+ model.name + ' ' + model.version,
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
        print(nodes)
        for level, x_list in nodes.items():
            GraphizController.render_instances(dot=dot, slots_data=[x[0] for x in x_list if x[0]])
        dot.graph_attr['root'] = str(nodes[0][0][1].id)
    
        dot.format = format
        return dot.pipe(encoding='utf-8')