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

@login_required
def index(request):
    template = loader.get_template("adminusers/index.html")
    context = {
        'error': False,
        'adminusers': []
    }
    try:
        metadata = get_tapis_config_metadata()
        context['adminusers'] = metadata['value']['admin_users']
    except Exception as e:
        context['error'] = True
        context['message'] = 'Admin user list could not be retrieved'
        logger.exception(e)
    return HttpResponse(template.render(context, request))


@login_required
def images(request, index):
    template = loader.get_template("adminusers/image.html")
    context = {
        'error': False,
        'index': index,
        'header': "JupyterHub Admin User Configuration",
        'adminuser': [],
        'api': reverse('adminusers:api', args=[str(index)])
    }
    try:
        metadata = get_tapis_config_metadata()
        adminuser = metadata['value']['admin_users'][index]
        context['adminuser'] = adminuser
        context['message'] = f"User {adminuser}"
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