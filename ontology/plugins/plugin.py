CAPABILITY_DUMMY = ''
CAPABILITY_IMPORT = 'IMPORT'
CAPABILITY_EXPORT = 'EXPORT'

class Plugin_v1:
    def capabilities():
        return [CAPABILITY_DUMMY]

    def get_format():
        return ('', '')

    def get_file_extension(knowledge_set):
        pass

    def import_ontology(model, path, filename='', filters=None):
        pass

    def export_ontology(model, path, filename='', filters=None):
        pass

    def import_instances(model, path, filename='', filters=None):
        pass

    def export_instances(model, path, filename='', filters=None):
        pass