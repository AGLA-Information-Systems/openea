class Utils:
    OBJECT_ORGANISATION = 'ORGA'
    OBJECT_PROFILE = 'PROF'
    OBJECT_TASK = 'TASK'
    OBJECT_SECURITY_GROUP = 'SECG'
    OBJECT_PERMISSION = 'PERM'
    OBJECT_REPOSITORY = 'REPO'
    OBJECT_MODEL = 'MODE'
    OBJECT_CONCEPT = 'CONC'
    OBJECT_RELATION = 'RELA'
    OBJECT_PREDICATE = 'PRED'
    OBJECT_INSTANCE = 'INST'
    OBJECT_REPORT = 'REPT'
    OBJECT_TAG_GROUP = 'TAGG'
    OBJECT_TAG = 'TAG'
    OBJECT_CONFIG = 'CONF'
    OBJECT_LOG = 'LOG'

    ADMIN_OBJECT_TYPE = [
        (OBJECT_PROFILE, 'Profile'),
        (OBJECT_TASK, 'Task'),
        (OBJECT_SECURITY_GROUP, 'Security Group'),
        (OBJECT_PERMISSION, 'Permission'),
        (OBJECT_REPOSITORY, 'Repository'),
        (OBJECT_MODEL, 'Model'),
        (OBJECT_CONCEPT, 'Concept'),
        (OBJECT_RELATION, 'Relation'),
        (OBJECT_PREDICATE, 'Predicate'),
        (OBJECT_INSTANCE, 'Instance'),
        (OBJECT_REPORT, 'Report'),
        (OBJECT_TAG_GROUP, 'Tag Group'),
        (OBJECT_TAG, 'Tag'),
        (OBJECT_CONFIG, 'Configuration'),
        (OBJECT_LOG, 'Log')
    ]

    SUPERADMIN_OBJECT_TYPE = [
        (OBJECT_ORGANISATION, 'Organisation')
    ]

    OBJECT_TYPE = SUPERADMIN_OBJECT_TYPE + ADMIN_OBJECT_TYPE
