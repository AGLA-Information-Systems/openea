from openea import OPENEA_VERSION
from django.conf import settings

def version_renderer(request):
    return {
       'openea_version': OPENEA_VERSION,
       'deployment_type': settings.DEPLOYMENT
    }