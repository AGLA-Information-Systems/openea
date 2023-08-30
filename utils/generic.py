from django.utils import timezone

from log.middleware.request import get_request
from openea.utils import Utils


def set_system_fields(obj, user, delete=False):
    if obj is not None and user is not None and user.is_authenticated:
        if obj.created_at is None:
            obj.created_by = user
            obj.created_at = timezone.now()
        
        obj.modified_by = user
        obj.modified_at = timezone.now()


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None
    
class GenericModel:
    def __init_subclass__(cls, **kwargs):
        from openea.utils import OBJECT_TYPES_REGISTRY
        OBJECT_TYPES_REGISTRY[cls.get_object_type()] = cls
        super().__init_subclass__(**kwargs)
    
    @classmethod
    def get_object_type(cls):
        return str(cls.__name__).upper()
    
    @classmethod
    def get_actions(cls):
        return [Utils.PERMISSION_ACTION_CREATE, Utils.PERMISSION_ACTION_LIST, Utils.PERMISSION_ACTION_VIEW, Utils.PERMISSION_ACTION_UPDATE, Utils.PERMISSION_ACTION_DELETE]


    def save(self, *args, **kwargs):
        new_object = True
        model_class = self.__class__
        field_names = [field.name for field in model_class._meta.fields if field.name not in ['created_at', 'created_by', 'modified_at', 'modified_by', 'deleted_at', 'deleted_by']]
        fields_stats = {}
        fields_changes = {}

        try:
            if self.pk is not None:
                orig = model_class.objects.get(pk=self.pk)
                new_object = False
                for field_name in field_names:
                    orig_field_value =  getattr(orig, field_name)
                    current_field_value = getattr(self, field_name)
                    fields_stats[field_name] = orig_field_value != current_field_value
                    if fields_stats[field_name]:
                        fields_changes[field_name] = (str(orig_field_value), str(current_field_value))
        except model_class.DoesNotExist:
            new_object = True

        
        log_object = []
        request = get_request()
        if request:
            log_object = request.log_object
            if request.user:
                set_system_fields(self, request.user)

        # The real thing
        super().save(*args, **kwargs)

        log_entry = {}
        if new_object:
            log_entry['source'] ='created '+ self.__class__.__name__
        else:
            log_entry['source'] ='updated '+ self.__class__.__name__
            log_entry['detail'] = str(fields_changes)
        log_entry['target'] = self.id
        log_entry['organisation'] = None
        if hasattr(self, 'organisation') and self.organisation is not None:
            log_entry['organisation'] = self.organisation
        log_object.append(log_entry)
        

    def delete(self, *args, **kwargs):
        log_object = []
        request = get_request()
        if request:
            log_object = request.log_object
            if request.user:
                self.deleted_by = request.user

        # The real thing
        #super().delete(*args, **kwargs)
        self.deleted_at = timezone.now()
        #super().save(*args, **kwargs)
        super().delete(*args, **kwargs)

        log_entry = {}
        log_entry['organisation'] = None
        if hasattr(self, 'organisation') and self.organisation is not None:
            log_entry['organisation'] = self.organisation
        log_entry['target'] = self.id
        log_entry['source'] = 'deleted '+ self.__class__.__name__
        log_object.append(log_entry)
