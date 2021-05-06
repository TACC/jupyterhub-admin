from django.http import HttpResponse
from django.template import loader
from jupyterhub_admin.metadata import get_config_metadata, write_config_metadata
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
        context['message'] = 'Image configuration could not be retrieved'
        logger.exception(e)
    return HttpResponse(template.render(context, request))


def images(request, index):
    template = loader.get_template("images/image.html")
    context = {
        'error': False,
        'index': index
    }
    try:
        metadata = get_config_metadata()
        context['image'] = metadata['value']['images'][index]
        context['message'] = f"Configuration for {context['image']['display_name']}" 
    except Exception as e:
        context['error'] = True
        context['message'] = 'Could not retrieve JupyterHub Image'
        logger.exception(e)
    return HttpResponse(template.render(context, request))


def new_image(request):
    template = loader.get_template("images/image.html")
    context = {
        'error': False,
        'index': 'new',
        'image': {
            'display_name': '',
            'image_name': ''
        },
        'message': f"Add a new JupyterHub Image"
    }
    return HttpResponse(template.render(context, request))


def api(request, index):
    if request.method == 'POST':
        display_name = request.POST.get('display_name')
        image_name = request.POST.get('image_name')
        try:
            metadata = get_config_metadata()
            image = {
                'display_name': display_name,
                'name': image_name
            }
            if index == 'new':
                metadata['value']['images'].append(image)
            else:
                index = int(index)
                metadata['value']['images'][index] = image
            write_config_metadata(metadata['value'])
            return HttpResponse("OK")
        except Exception as e:
            logger.exception(e)
            return HttpResponse(status=500)
    
    if request.method == 'DELETE':
        try:
            index = int(index)
            metadata = get_config_metadata()
            metadata['value']['images'].pop(index)
            write_config_metadata(metadata['value'])
            return HttpResponse("OK")
        except Exception as e:
            logger.exception(e)
            return HttpResponse(status=500)
            