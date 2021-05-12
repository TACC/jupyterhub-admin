import pytest
from unittest.mock import MagicMock, ANY


@pytest.fixture
def metadata():
    yield {
      'uuid': 'MOCK_UUID',
      'name': 'MOCK_NAME',
      'value': {
            'volume_mounts': [
                {
                    'type': 'hostPath',
                    'path': '/local/path',
                    'mountPath': '/jupyter/path0',
                    'readOnly': 'False'
                },
                {
                    'type': 'nfs',
                    'server': 'nfs.host',
                    'path': '/nfs/path',
                    'mountPath': '/jupyter/path1',
                    'readOnly': 'True'
                }
                
            ]
        }
    }


@pytest.fixture
def get_config_metadata(mocker, metadata):
    yield mocker.patch('jupyterhub_admin.apps.mounts.views.get_config_metadata', return_value=metadata)


@pytest.fixture
def write_config_metadata(mocker):
    yield mocker.patch('jupyterhub_admin.apps.mounts.views.write_config_metadata')


@pytest.fixture
def template_render(mocker):
    mock_get_template = MagicMock()
    mock_render = MagicMock()
    mock_get_template.render = mock_render
    mocker.patch('jupyterhub_admin.apps.mounts.views.loader.get_template', return_value=mock_get_template)
    yield mock_render


def test_index(client, template_render, get_config_metadata, metadata):
    context = {
        'error': False,
        'mounts': [
            {
                'mountPath': '/jupyter/path0',
                'path': '/local/path'
            },
            {
                'mountPath': '/jupyter/path1',
                'path': 'nfs://nfs.host/nfs/path'
            }
        ]
    }
    response = client.get('/mounts/')
    template_render.assert_called_with(context, ANY)


def test_mounts(client, template_render, get_config_metadata, metadata):
    context = {
        'error': False,
        'index': 1,
        'header': "JupyterHub Mount Configuration",
        'fields': [
            {
                'label': 'Mount Type',
                'id': 'mount_type',
                'value': 'nfs',
                'type': 'select',
                'options': [ {'value': 'hostPath', 'label': 'Host Path'}, {'value': 'nfs', 'label': 'NFS' }],
                'placeholder': 'The type of file system mount'
            },
            {
                'label': 'Remote Server',
                'id': 'server',
                'value': 'nfs.host',
                'type': 'text',
                'placeholder': 'The hostname of the remote server for this mount'
            },
            {
                'label': 'Path',
                'id': 'path',
                'type': 'text',
                'value': '/nfs/path',
                'placeholder': 'The path on the JupyterHub host',
            },
            {
                'label': 'Mount Path',
                'id': 'mount_path',
                'value': '/jupyter/path1',
                'type': 'text',
                'placeholder': 'The path for this mount on the Jupyter server'
            },
            {
                'label': 'Read Only',
                'id': 'read_only',
                'value': True,
                'type': 'checkbox',
                'placeholder': 'If true, the server will not allow notebook writes to this path'
            }
        ],
        'message': 'Configuration for /jupyter/path1',
        'api': '/mounts/api/1',
        'delete_confirmation': '/jupyter/path1'
    }
    response = client.get('/mounts/1')
    template_render.assert_called_with(context, ANY)


def test_api_post(client, get_config_metadata, write_config_metadata, metadata):
    data = {
        'mount_type': 'hostPath',
        'server': 'IGNORED',
        'path': '/host/path',
        'mount_path': '/jupyter/mount',
        'read_only': 'true'
    }
    expected = metadata['value'].copy()
    expected['volume_mounts'][1] = {
        'type': 'hostPath',
        'path': '/host/path',
        'mountPath': '/jupyter/mount',
        'readOnly': 'True'
    }
    response = client.post('/mounts/api/1', data=data)
    assert response.status_code == 200
    write_config_metadata.assert_called_with(expected)


def test_api_post_nfs(client, get_config_metadata, write_config_metadata, metadata):
    data = {
        'mount_type': 'nfs',
        'server': 'nfs.host',
        'path': '/host/path',
        'mount_path': '/jupyter/mount',
        'read_only': 'true'
    }
    expected = metadata['value'].copy()
    expected['volume_mounts'][1] = {
        'type': 'nfs',
        'server': 'nfs.host',
        'path': '/host/path',
        'mountPath': '/jupyter/mount',
        'readOnly': 'True'
    }
    response = client.post('/mounts/api/1', data=data)
    assert response.status_code == 200
    write_config_metadata.assert_called_with(expected)


def test_api_new(client, get_config_metadata, write_config_metadata, metadata):
    data = {
        'mount_type': 'nfs',
        'server': 'nfs.host',
        'path': '/host/path',
        'mount_path': '/jupyter/mount',
        'read_only': 'true'
    }
    expected = metadata['value'].copy()
    expected['volume_mounts'].append({
        'type': 'nfs',
        'server': 'nfs.host',
        'path': '/host/path',
        'mountPath': '/jupyter/mount',
        'readOnly': 'True'
    })
    response = client.post('/mounts/api/new', data=data)
    assert response.status_code == 200
    write_config_metadata.assert_called_with(expected)


def test_api_delete(client, get_config_metadata, write_config_metadata, metadata):
    response = client.delete('/mounts/api/1')
    assert response.status_code == 200
    write_config_metadata.assert_called_with({
        'volume_mounts': [
            {
                'type': 'hostPath',
                'path': '/local/path',
                'mountPath': '/jupyter/path0',
                'readOnly': 'False'
            }
        ]
    })
