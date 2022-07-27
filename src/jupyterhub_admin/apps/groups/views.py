from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.urls import reverse
from jupyterhub_admin.metadata import (
    list_tapis_group_config_metadata,
    write_tapis_group_config_metadata,
    create_tapis_group_config_metadata,
    get_tapis_group_config_metadata,
    rename_tapis_group_config_metadata,
    delete_tapis_group_config_metadata
)
from django.contrib.auth.decorators import login_required
import logging
import json
from jupyterhub_admin.apps.mounts.views import get_fields as get_mount_fields
from jupyterhub_admin.jhub_api import stop_server, stop_specified_server, get_user


logger = logging.getLogger(__name__)


@login_required
def index(request):
    template = loader.get_template("groups/index.html")
    context = {
        'error': False,
        'groups': []
    }
    try:
        metadata = list_tapis_group_config_metadata()

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
        metadata = list_tapis_group_config_metadata()

        context['group'] = get_tapis_group_config_metadata(group)['value']
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
    create_tapis_group_config_metadata(group)
    url = reverse('groups:groups', args=[group])
    return JsonResponse({ 'url': url })


@login_required
def rename_group(request):
    content = json.loads(request.body)
    original = content['previousName']
    group = content['group']
    rename_tapis_group_config_metadata(original, group)
    url = reverse('groups:groups', args=[group])
    return JsonResponse({ 'url': url })


@login_required
def delete_group(request):
    content = json.loads(request.body)
    group = content['group']
    delete_tapis_group_config_metadata(group)
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
def stop_all_servers(request):
    content = json.loads(request.body)
    group = content['group']
    meta = get_tapis_group_config_metadata(group)
    users = meta['value']['user']
    for username in users:
        user = get_user(username)
        if user['servers'] is not None:
            for server in user['servers']:
                stop_specified_server(username, server)
        else:
            stop_server(username)
    url = reverse('groups:groups', args=[group])
    return JsonResponse({ 'url': url})

@login_required
def user(request, group, index):
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
        meta = get_tapis_group_config_metadata(group)
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
def images(request, group, index):
    fields = [
        {
            'label': 'Display Name',
            'id': 'display_name',
            'value': '',
            'type': 'text',
            'placeholder': "Name of the image to display in the spawner"
        },
        {
            'label': 'Image Name',
            'id': 'image_name',
            'value': '',
            'type': 'text',
            'placeholder': "Image repository, name and tag"
        }
    ]
    template = loader.get_template("groups/image.html")
    context = {
        'error': False,
        'index': index,
        'header': f"User Group {group}",
        'fields': fields,
        'group': group,
        'api': reverse('groups:images_api', args=[group, str(index)])
    }
    try:
        meta = get_tapis_group_config_metadata(group)
        if index == 'new':
            context['message'] = "Add a new image for this group"
            context['delete_confirmation'] = ""
        else:
            image = meta['value']['images'][int(index)]
            display_name = image['display_name']
            image_name = image['name']
            context['fields'][0]['value'] = display_name
            context['fields'][1]['value'] = image_name
            context['message'] = f"Edit group image {display_name}"
            context['delete_confirmation'] = f"image {display_name} from {group}"
    except Exception as e:
        context['error'] = True
        context['message'] = f"Could not retrieve image in group {group}"
        logger.exception(e)
    return HttpResponse(template.render(context, request))


@login_required
def mounts(request, group, index):
    template = loader.get_template("groups/mount.html")
    context = {
        'error': False,
        'index': index,
        'header': f"User Group {group}",
        'fields': get_mount_fields(),
        'group': group,
        'api': reverse('groups:mounts_api', args=[group, str(index)])
    }
    try:
        if index == 'new':
            context['message'] = "Add a new volume mount for this group"
            context['delete_confirmation'] = ""
        else:
            index = int(index)
            metadata = get_tapis_group_config_metadata(group)
            mount = metadata['value']['volume_mounts'][index]
            context['fields'] = get_mount_fields(mount)
            context['message'] = f"Configuration for group mount {mount['mountPath']}"
            context['delete_confirmation'] = f"{mount['mountPath']} from group {group}"
    except Exception as e:
        context['error'] = True
        context['message'] = 'Could not retrieve group volume mount'
        logger.exception(e)
    return HttpResponse(template.render(context, request))


@login_required
def user_api(request, group, index):
    if request.method == 'POST':
        user = request.POST.get('user')
        try:
            metadata = get_tapis_group_config_metadata(group)
            if index == 'new':
                metadata['value']['user'].append(user)
            else:
                index = int(index)
                metadata['value']['user'][index] = user
            write_tapis_group_config_metadata(group, metadata['value'])
            return JsonResponse(data = {'url': reverse('groups:groups', args=[group])})
        except Exception as e:
            logger.exception(e)
            return HttpResponse(status=500)

    if request.method == 'DELETE':
        try:
            index = int(index)
            metadata = get_tapis_group_config_metadata(group)
            metadata['value']['user'].pop(index)
            write_tapis_group_config_metadata(group, metadata['value'])
            return JsonResponse(data = {'url': reverse('groups:groups', args=[group])})
        except Exception as e:
            logger.exception(e)
            return HttpResponse(status=500)


@login_required
def images_api(request, group, index):
    if request.method == 'POST':
        display_name = request.POST.get('display_name')
        image_name = request.POST.get('image_name')
        try:
            metadata = get_tapis_group_config_metadata(group)
            image = {
                'display_name': display_name,
                'name': image_name
            }
            if index == 'new':
                metadata['value']['images'].append(image)
            else:
                index = int(index)
                metadata['value']['images'][index] = image
            write_tapis_group_config_metadata(group, metadata['value'])
            return JsonResponse(data = {'url': reverse('groups:groups', args=[group])})
        except Exception as e:
            logger.exception(e)
            return HttpResponse(status=500)

    if request.method == 'DELETE':
        try:
            index = int(index)
            metadata = get_tapis_group_config_metadata(group)
            metadata['value']['images'].pop(index)
            write_tapis_group_config_metadata(group, metadata['value'])
            return JsonResponse(data = {'url': reverse('groups:groups', args=[group])})
        except Exception as e:
            logger.exception(e)
            return HttpResponse(status=500)


@login_required
def mounts_api(request, group, index):
    if request.method == 'POST':
        try:
            metadata = get_tapis_group_config_metadata(group)
            mount = {
                'type': request.POST.get('mount_type'),
                'path': request.POST.get('path'),
                'mountPath': request.POST.get('mount_path'),
                'readOnly': "True" if request.POST.get('read_only') == 'true' else "False"
            }
            if (mount['type'] == 'nfs'):
                mount['server'] = request.POST.get('server')
            if index == 'new':
                metadata['value']['volume_mounts'].append(mount)
            else:
                index = int(index)
                metadata['value']['volume_mounts'][index] = mount
            write_tapis_group_config_metadata(group, metadata['value'])
            return JsonResponse(data = {'url': reverse('groups:groups', args=[group])})
        except Exception as e:
            logger.exception(e)
            return HttpResponse(status=500)

    if request.method == 'DELETE':
        try:
            index = int(index)
            metadata = get_tapis_group_config_metadata(group)
            metadata['value']['volume_mounts'].pop(index)
            write_tapis_group_config_metadata(group, metadata['value'])
            return JsonResponse(data = {'url': reverse('groups:groups', args=[group])})
        except Exception as e:
            logger.exception(e)
            return HttpResponse(status=500)
