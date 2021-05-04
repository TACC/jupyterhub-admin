from django.http import HttpResponse
from django.template import loader
from jupyterhub_admin.metadata import get_config_metadata
import logging


logger = logging.getLogger(__name__)


def index(request):
    template = loader.get_template("images/index.html")
    context = {
        'error': False,
        'images': []
    }
    try:
        metadata = get_config_metadata()
        context['images'] = metadata['value']['images']
    except Exception as e:
        context['error'] = True
        logger.exception()
    return HttpResponse(template.render(context, request))

def image(request, index):
    return HttpResponse(str(index))