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


def get_user_fields(user):
    return [
        {
            'label': 'User Name',
            'id': 'user',
            'value': user if user else '',
            'type': 'text',
            'placeholder': "Username"
        }
    ]


@login_required
def user(request, group, index):
    # TODO process user as 'new' or index
    fields = [
        {
            'label': 'User Name',
            'id': 'user',
            'value': '',
            'type': 'text',
            'placeholder': "Username"
        }
    ]
    template = loader.get_template("groups/user.html")
    context = {
        'error': False,
        'index': index,
        'header': f"User Group {group}",
        'fields': fields,
        'group': group,
        'api': reverse('groups:user_api', args=[group, str(index)])
    }
    try:
        meta = get_group_config_metadata(group)
        if index == 'new':
            context['message'] = "Add a new group member"
            context['delete_confirmation'] = ""
        else:
            username = meta['value']['user'][int(index)]
            context['fields'][0]['value'] = username
            context['message'] = f"Edit group member {username}"
            context['delete_confirmation'] = f"{username} from {group}"
    except Exception as e:
        context['error'] = True
        context['message'] = f"Could not retrieve user in group {group}"
        logger.exception(e)
    return HttpResponse(template.render(context, request))


@login_required
def user_api(request, group, index):
    if request.method == 'POST':
        user = request.POST.get('user')
        try:
            metadata = get_group_config_metadata(group)
            if index == 'new':
                metadata['value']['user'].append(user)
            else:
                index = int(index)
                metadata['value']['user'][index] = user
            write_group_config_metadata(group, metadata['value'])
            return JsonResponse(data = {'url': reverse('groups:groups', args=[group])})
        except Exception as e:
            logger.exception(e)
            return HttpResponse(status=500)
    
    if request.method == 'DELETE':
        try:
            index = int(index)
            metadata = get_group_config_metadata(group)
            metadata['value']['user'].pop(index)
            write_group_config_metadata(group, metadata['value'])
            return JsonResponse(data = {'url': reverse('groups:groups', args=[group])})
        except Exception as e:
            logger.exception(e)
            return HttpResponse(status=500)
