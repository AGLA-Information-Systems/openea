from datetime import datetime
from django.http import HttpResponse


def set_system_fields(instance, user):
    if instance is not None and user is not None:
        if instance.id:
            instance.created_by = user
            instance.created_at = datetime.now
        else:
            instance.modified_by = user
            instance.modified_on = datetime.now

def handle_errors(function):
    def wrapper(*args,**kwargs):
        try:
            return function(*args,**kwargs)
        except Exception as e:
            return HttpResponse('Exception:'+str(e))
    return wrapper


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None