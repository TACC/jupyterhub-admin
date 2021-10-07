from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from jupyterhub_admin.metadata import get_tapis_config_metadata, write_tapis_config_metadata
from django.contrib.auth.decorators import login_required
import logging
import copy


logger = logging.getLogger(__name__)


def get_fields(mount=None):
    return [
        {
            'label': 'Mount Type',
            'id': 'mount_type',
            'value': 'hostPath' if not mount else mount['type'],
            'type': 'select',
            'options': [ {'value': 'hostPath', 'label': 'Host Path'}, {'value': 'nfs', 'label': 'NFS' }],
            'placeholder': 'The type of file system mount'
        },
        {
            'label': 'Remote Server',
            'id': 'server',
            'value': '' if not mount or 'server' not in mount else mount['server'],
            'type': 'text',
            'placeholder': 'The hostname of the remote server for this mount'
        },
        {
            'label': 'Path',
            'id': 'path',
            'type': 'text',
            'value': '' if not mount else mount['path'],
            'placeholder': 'The path on the JupyterHub host',
        },
        {
            'label': 'Mount Path',
            'id': 'mount_path',
            'value': '' if not mount or not mount['mountPath'] else mount['mountPath'],
            'type': 'text',
            'placeholder': 'The path for this mount on the Jupyter server'
        },
        {
            'label': 'Read Only',
            'id': 'read_only',
            'value': True if not mount else mount['readOnly'] == "True",
            'type': 'checkbox',
            'placeholder': 'If true, the server will not allow notebook writes to this path'
        }
    ]


@login_required
def index(request):
    template = loader.get_template("mounts/index.html")
    context = {
        'error': False,
        'mounts': []
    }
    try:
        metadata = get_tapis_config_metadata()
        mounts = metadata['value']['volume_mounts']
        for mount in mounts:
            if mount['type'] != 'hostPath':
                hostpath = f"{mount['type']}://{mount['server']}{mount['path']}"
            else:
                hostpath = mount['path']
            context['mounts'].append({
                'path': hostpath,
                'mountPath': mount['mountPath']
            })
    except Exception as e:
        context['error'] = True
        context['message'] = 'Mount configuration could not be retrieved'
        logger.exception(e)
    return HttpResponse(template.render(context, request))


@login_required
def mounts(request, index):
    template = loader.get_template("mounts/mount.html")
    context = {
        'error': False,
        'index': index,
        'header': "JupyterHub Mount Configuration",
        'fields': [],
        'api': reverse('mounts:api', args=[str(index)])
    }
    try:
        metadata = get_tapis_config_metadata()
        mount = metadata['value']['volume_mounts'][index]
        context['fields'] = get_fields(mount)
        context['message'] = f"Configuration for {mount['mountPath']}"
        context['delete_confirmation'] = f"{mount['mountPath']}"
    except Exception as e:
        context['error'] = True
        context['message'] = 'Could not retrieve JupyterHub Volume Mount'
        logger.exception(e)
    return HttpResponse(template.render(context, request))


@login_required
def new_mount(request):
    template = loader.get_template("mounts/mount.html")
    context = {
        'error': False,
        'index': 'new',
        'fields': get_fields(),
        'api': reverse('mounts:api', args=["new"]),
        'header': f"JupyterHub Volume Mount Configuration",
        'message': f"Add a new JupyterHub Volume Mount",
    }
    return HttpResponse(template.render(context, request))


@login_required
def api(request, index):
    if request.method == 'POST':
        try:
            metadata = get_tapis_config_metadata()
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
            write_tapis_config_metadata(metadata['value'])
            return HttpResponse("OK")
        except Exception as e:
            logger.exception(e)
            return HttpResponse(status=500)

    if request.method == 'DELETE':
        try:
            index = int(index)
            metadata = get_tapis_config_metadata()
            metadata['value']['volume_mounts'].pop(index)
            write_tapis_config_metadata(metadata['value'])
            return HttpResponse("OK")
        except Exception as e:
            logger.exception(e)
            return HttpResponse(status=500)
