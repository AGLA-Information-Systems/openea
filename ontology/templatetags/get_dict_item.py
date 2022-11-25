from django.template import Library

register = Library()


@register.filter
def get_dict_item(dictionary, key):
    return dictionary.get(key, None)