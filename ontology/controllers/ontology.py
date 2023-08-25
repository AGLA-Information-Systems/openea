


CLASS_ROLE_ABSTRACT = 'ABSTRACT'
CLASS_ROLE_CONCRETE = 'CONCRETE'
CLASS_ROLE  = [
    (CLASS_ROLE_ABSTRACT, 'Abstract'),
    (CLASS_ROLE_CONCRETE, 'Concrete')
]
CLASS_ROLES = set([CLASS_ROLE_ABSTRACT, CLASS_ROLE_CONCRETE])

VALUE_TYPE_STRING = 'STRING'
VALUE_TYPE_NUMBER = 'NUMBER'
VALUE_TYPE_BOOLEAN = 'BOOLEAN'
VALUE_TYPE_ENUMERATED = 'ENUMERATED'
VALUE_TYPE_INSTANCE = 'INSTANCE'
VALUE_TYPE  = [
    (VALUE_TYPE_STRING, 'String'),
    (VALUE_TYPE_NUMBER, 'Number'),
    (VALUE_TYPE_BOOLEAN, 'Boolean'),
    (VALUE_TYPE_ENUMERATED, 'Enumerated'),
    (VALUE_TYPE_INSTANCE, 'Instance'),
]
VALUE_TYPES = set([VALUE_TYPE_STRING, VALUE_TYPE_NUMBER, VALUE_TYPE_BOOLEAN, VALUE_TYPE_ENUMERATED, VALUE_TYPE_INSTANCE])
NATIVE_VALUE_TYPES = set([VALUE_TYPE_STRING, VALUE_TYPE_NUMBER, VALUE_TYPE_BOOLEAN, VALUE_TYPE_ENUMERATED])

CARDINALITY_SINGLE = 'SINGLE'
CARDINALITY_MULTIPLE = 'MULTIPLE'
CARDINALITY  = [
    (CARDINALITY_SINGLE, 'Single'),
    (CARDINALITY_MULTIPLE, 'Multiple')
]
CARDINALITIES = set([CARDINALITY_SINGLE, CARDINALITY_MULTIPLE])

class KnowledgeBase:
    pass

class OClass:
    def __init__(self, id, name, description, role, is_a, concept):
        self.id = id
        self.name = name
        self.description = description
        if role not in CLASS_ROLES:
            raise ValueError('INVALID_CLASS_ROLES:' + str(role))
        self.role = role
        self.is_a = is_a
        self.concept = concept

    def get_or_create(name):
        raise NotImplementedError
    
    def __str__(self):
        return self.name

class OSlot:
    """
    
    """
    def __init__(self, id, name, description, cardinality, allowed_values, value_type, value, objects, oclass, concept):
        self.id = id
        self.name = name
        self.description = description
        if cardinality not in CARDINALITIES:
            raise ValueError('INVALID_CARDINALITY:' + str(cardinality))
        self.cardinality = cardinality
        self.allowed_values = allowed_values
        if value_type not in VALUE_TYPES:
            raise ValueError('INVALID_VALUE_TYPE:' + str(value_type))
        self.value_type = value_type 
        self.value = value
        self.objects = objects
        self.oclass = oclass
        self.concept = concept

    def get_value():
        if self.oslot.value_type in NATIVE_VALUE_TYPES:
            return self.value
        elif self.oslot.value_type is VALUE_TYPE_INSTANCE:
            return self.objects

    def __str__(self):
        return self.name


class OFacet(GenericModel, models.Model):
    def __init__(self, id, name, description, value, oslot, concept):
        self.id = id
        self.name = name
        self.description = description
        self.value = value
        self.objects = objects
        self.oslot = oslot
        self.concept = concept
    
    def __str__(self):
        return self.name
