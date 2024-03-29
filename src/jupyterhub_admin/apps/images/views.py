from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from jupyterhub_admin.metadata import (
    get_tapis_config_metadata,
    write_tapis_config_metadata
)
from django.contrib.auth.decorators import login_required
import logging
import copy


logger = logging.getLogger(__name__)


def get_fields(image=None):
    return [
        {
            'label': 'Display Name',
            'id': 'display_name',
            'value': '' if not image else image['display_name'],
            'type': 'text',
            'placeholder': "Name of the image to display in the spawner"
        },
        {
            'label': 'Image Name',
            'id': 'image_name',
            'value': '' if not image else image['name'],
            'type': 'text',
            'placeholder': "Image repository, name and tag"
        }
    ]


@login_required
def index(request):
    template = loader.get_template("images/index.html")
    context = {
        'error': False,
        'images': []
    }
    try:
        metadata = get_tapis_config_metadata()
        context['images'] = metadata['value']['images']
    except Exception as e:
        context['error'] = True
        context['message'] = 'Image configuration could not be retrieved'
        logger.exception(e)
    return HttpResponse(template.render(context, request))


@login_required
def images(request, index):
    template = loader.get_template("images/image.html")
    context = {
        'error': False,
        'index': index,
        'header': "JupyterHub Image Configuration",
        'fields': [],
        'api': reverse('images:api', args=[str(index)])
    }
    try:
        metadata = get_tapis_config_metadata()
        image = metadata['value']['images'][index]
        context['fields'] = get_fields(image)
        context['message'] = f"Configuration for {image['display_name']}"
        context['delete_confirmation'] = f"{image['display_name']} ({image['name']})"
    except Exception as e:
        context['error'] = True
        context['message'] = 'Could not retrieve JupyterHub Image'
        logger.exception(e)
    return HttpResponse(template.render(context, request))


@login_required
def new_image(request):
    template = loader.get_template("images/image.html")
    context = {
        'error': False,
        'index': 'new',
        'fields': get_fields(),
        'api': reverse('images:api', args=["new"]),
        'header': f"JupyterHub Image Configuration",
        'message': f"Add a new JupyterHub Image",
    }
    return HttpResponse(template.render(context, request))


@login_required
def api(request, index):
    if request.method == 'POST':
        display_name = request.POST.get('display_name')
        image_name = request.POST.get('image_name')
        try:
            metadata = get_tapis_config_metadata()
            image = {
                'display_name': display_name,
                'name': image_name
            }
            if index == 'new':
                metadata['value']['images'].append(image)
            else:
                index = int(index)
                metadata['value']['images'][index] = image
            write_tapis_config_metadata(metadata['value'])
            return HttpResponse("OK")
        except Exception as e:
            logger.exception(e)
            return HttpResponse(status=500)

    if request.method == 'DELETE':
        try:
            index = int(index)
            metadata = get_tapis_config_metadata()
            metadata['value']['images'].pop(index)
            write_tapis_config_metadata(metadata['value'])
            return HttpResponse("OK")
        except Exception as e:
            logger.exception(e)
            return HttpResponse(status=500)
