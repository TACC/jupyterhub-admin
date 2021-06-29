from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.urls import reverse
from jupyterhub_admin.metadata import (
    list_group_config_metadata,
    write_group_config_metadata,
    create_group_config_metadata,
    get_group_config_metadata,
    rename_group_config_metadata,
    delete_group_config_metadata
)
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
        context['groups'] = [
            {
                'group': group['value']['group_name'],
                'users': len(group['value']['user']),
                'images': len(group['value']['images']),
                'volume_mounts': len(group['value']['volume_mounts']),
            } for group in metadata
        ]
        context['existing'] = [ group['value']['group_name'] for group in metadata ]
        context['groupNameApi'] = reverse('groups:create_group')
    except Exception as e:
        context['error'] = True
        context['message'] = 'Groups could not be retrieved'
        logger.exception(e)
    return HttpResponse(template.render(context, request))


@login_required
def groups(request, group):
    template = loader.get_template("groups/group.html")
    context = {
        'error': False,
    }
    try:
        metadata = list_group_config_metadata()
        context['group'] = get_group_config_metadata(group)['value']
        context['existing'] = [ group['value']['group_name'] for group in metadata ]
        context['groupNameApi'] = reverse('groups:rename_group')
    except Exception as e:
        context['error'] = True
        context['message'] = 'ERROR: Group could not be retrieved'
    return HttpResponse(template.render(context, request))


@login_required
def create_group(request):
    content = json.loads(request.body)
    group = content['group']
    create_group_config_metadata(group)
    url = reverse('groups:groups', args=[group])
    return JsonResponse({ 'url': url })


@login_required
def rename_group(request):
    content = json.loads(request.body)
    original = content['previousName']
    group = content['group']
    rename_group_config_metadata(original, group)
    url = reverse('groups:groups', args=[group])
    return JsonResponse({ 'url': url })


@login_required
def delete_group(request):
    content = json.loads(request.body)
    group = content['group']
    delete_group_config_metadata(group)
    return JsonResponse({ 'url': reverse('groups:index')})


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
            
