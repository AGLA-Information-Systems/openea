from configuration.models import Setting
from ontology.models import OConcept
from openea.utils import Utils


class ConfigutationController():
    def get_tag_groups_configurations(organisation):
        default_tag_group_configs = []
        for object_type in Utils.DEFAULT_OBJECT_TYPE:
            default_tag_group_configs.append('tag_group__' + object_type[0])
        for concept in OConcept.objects.filter(organisation):
            default_tag_group_configs.append('tag_group__' + Utils.OBJECT_CONCEPT + '__' + concept.id)
        
        settings = Setting.objects.filter(organisation, name__startswith='tag_group__*')

