import textwrap as tr

import graphviz
from django.conf import settings

from ontology.controllers.o_model import ModelUtils

palette = ['#eeefef', '#fff3bf', '#d5ecc0', '#a2e0ec']
class GraphvizController:
    
    def render_model_graph (format, model_data, knowledge_set='instances'):
        if not format:
            format = 'svg'

        model = model_data.get('model')
        node_colors = {}
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
                                    'nodesep':'0.1',
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
                                    'gradientangle':'90',
                                    'fillcolor': '#eeefef:white'},
                                edge_attr={
                                    'fontname': 'arial',
                                    'len': '2.0',
                                    'minlen': '1.0',
                                    'fontsize': '12',
                                    'color': '#6c757d',
                                    'fontcolor': '#212529'})
        
        if knowledge_set == 'ontology':
            GraphvizController.render_ontology (dot, node_colors=node_colors, slots_data=model_data['predicates'])
        elif knowledge_set == 'instances':
            GraphvizController.render_instances (dot, node_colors=node_colors, slots_data=model_data['slots'])
        
        #dot_ = dot.unflatten(stagger=1)
        dot.format = format
        return dot.pipe(encoding='utf-8')

    def render_ontology (dot, node_colors, predicates_data):
        nbr_edges = 0
        for predicate in predicates_data:
            node_color = GraphvizController.get_node_color(node_colors, predicate.subject.concept.id)
            dot.node(str(predicate.subject.id), label=GraphvizController.get_concept_label(predicate.subject), href=ModelUtils.get_url('concept', predicate.subject.id), fillcolor="{}:{}".format(node_color,'white'))
            node_color = GraphvizController.get_node_color(node_colors, predicate.object.concept.id)
            dot.node(str(predicate.object.id), label=GraphvizController.get_concept_label(predicate.object), href=ModelUtils.get_url('concept', predicate.object.id), fillcolor="{}:{}".format(node_color,'white'))
            dot.edge(str(predicate.subject.id), str(predicate.object.id), label=GraphvizController.get_relation_label(predicate.relation), href=ModelUtils.get_url('predicate', predicate.id))
            if nbr_edges >= settings.MAX_GRAPH_NODES:
                break
            nbr_edges =+ 1

    def render_instances (dot, node_colors, slots_data):
        nbr_edges = 0
        for slot in slots_data:
            if slot.subject is not None:
                node_color = GraphvizController.get_node_color(node_colors, slot.subject.concept.id)
                dot.node(str(slot.subject.id), label=GraphvizController.get_instance_label(slot.subject), href=ModelUtils.get_url('instance', slot.subject.id), fillcolor="{}:{}".format(node_color,'white'))
            if slot.object is not None:
                node_color = GraphvizController.get_node_color(node_colors, slot.object.concept.id)
                dot.node(str(slot.object.id), label=GraphvizController.get_instance_label(slot.object), href=ModelUtils.get_url('instance', slot.object.id), fillcolor="{}:{}".format(node_color,'white'))
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
        node_colors = {}
        dot = graphviz.Digraph( engine='sfdp',
                                comment='OpenEA',
                                graph_attr={
                                    'id': 'modelgraph',
                                    'label': GraphvizController.get_graph_label(model),
                                    'repulsiveforce': '0.5',
                                    'overlap': 'false',
                                    'splines': 'true',
                                    'concentrate': 'true',
                                    #'splines': 'curved',
                                    'ranksep':'1.5 equally',
                                    'fontname': 'arial',
                                    'fontsize': '12',
                                    'fontcolor': '#212529'},
                                node_attr={
                                    'style':'filled',
                                    'gradientangle':'90',
                                    'maxTextWidth': '3.3',
                                    'fontname': 'arial',
                                    'fontsize': '12',
                                    'color': '#6c757d',
                                    'fontcolor': '#212529',
                                    'fillcolor': '#eeefef:white'},
                                edge_attr={
                                    'fontname': 'arial',
                                    'fontsize': '12',
                                    #'len': '2.0',
                                    #'minlen': '1.0',
                                    'color': '#6c757d',
                                    'fontcolor': '#212529'})
        for level, x_list in nodes.items():
            GraphvizController.render_instances(dot=dot, node_colors=node_colors, slots_data=[x[0] for x in x_list if x[0]])
        dot.graph_attr['root'] = str(nodes[0][0][1].id)
    
        dot.format = format
        return dot.pipe(encoding='utf-8')

    def get_node_color(node_colors, node_id):
        if node_id not in node_colors:
            new_index = len(node_colors) % len(palette)
            node_colors[node_id] = palette[new_index]
        return node_colors[node_id]
