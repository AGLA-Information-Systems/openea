ACTION_DUMMY = ''
ACTION_IMPORT = 'IMPORT'
ACTION_EXPORT = 'EXPORT'

class Plugin:
    def available_actions():
        return [ACTION_DUMMY]

    def get_format():
        return ('', '')

    def get_file_extension(knowledge_set):
        pass

    def import_ontology(model, path, filename=''):
        pass

    def export_ontology(model, path, filename=''):
        pass

    def import_instances(model, path, filename=''):
        pass

    def export_instances(model, path, filename=''):
        pass