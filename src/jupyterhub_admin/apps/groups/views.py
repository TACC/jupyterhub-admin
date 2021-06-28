from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.urls import reverse
from jupyterhub_admin.metadata import list_group_config_metadata
from django.contrib.auth.decorators import login_required
import logging
import json


logger = logging.getLogger(__name__)


def get_fields(group=None):
    return [
        {
            'label': 'Group Name',
            'id': 'group',
            'value': '' if not group else group['group'],
            'type': 'text',
            'placeholder': "Name of the user group"
        }
    ]


@login_required
def index(request):
    template = loader.get_template("groups/index.html")
    context = {
        'error': False,
        'groups': []
    }
    try:
        metadata = list_group_config_metadata()
        existing = json.dumps([ group['group'] for group in metadata])
        print("EXISTING", existing);
        context['groups'] = [
            {
                'group': group['group'],
                'users': len(group['user']),
                'images': len(group['images']),
                'volume_mounts': len(group['volume_mounts']),
                'existing': existing
            } for group in metadata
        ]
    except Exception as e:
        context['error'] = True
        context['message'] = 'Groups could not be retrieved'
        logger.exception(e)
    return HttpResponse(template.render(context, request))


@login_required
def groups(request, group):
    pass
"""
    template = loader.get_template("images/image.html")
    context = {
        'error': False,
        'index': index,
        'header': "JupyterHub Image Configuration",
        'fields': [],
        'api': reverse('images:api', args=[str(index)])
    }
    try:
        metadata = get_config_metadata()
        image = metadata['value']['images'][index]
        context['fields'] = get_fields(image)
        context['message'] = f"Configuration for {image['display_name']}" 
        context['delete_confirmation'] = f"{image['display_name']} ({image['name']})"
    except Exception as e:
        context['error'] = True
        context['message'] = 'Could not retrieve JupyterHub Image'
        logger.exception(e)
    return HttpResponse(template.render(context, request))
"""
@login_required
def new_image(request):
    template = loader.get_template("groups/group.html")
    metadata = list_group_config_metadata()
    existing = [ group['group'] for group in metadata ]
    context = {
        'error': False,
        'group': 'new',
        'existing': existing,
        'fields': get_fields(),
        'api': reverse('groups:api', args=["group"]),
        'header': f"User Group Settings",
        'message': f"Add a new User Group",
    }
    return HttpResponse(template.render(context, request))


@login_required
def api(request, group):
    return JsonResponse(data = {'url': group})
    """
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
    """
            
