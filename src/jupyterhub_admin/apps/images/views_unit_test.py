import pytest
from unittest.mock import MagicMock, ANY


@pytest.fixture
def metadata():
    yield {
      'uuid': 'MOCK_UUID',
      'name': 'MOCK_NAME',
      'value': {
          'images': [
              {
                  'display_name': "Image 0",
                  'name': 'org/repo0:tag'
              },
              {
                  'display_name': "Image 1",
                  'name': 'org/repo1:tag'
              }
          ]
      }
    }


@pytest.fixture
def get_config_metadata(mocker, metadata):
    yield mocker.patch('jupyterhub_admin.apps.images.views.get_config_metadata', return_value=metadata)


@pytest.fixture
def write_config_metadata(mocker):
    yield mocker.patch('jupyterhub_admin.apps.images.views.write_config_metadata')


@pytest.fixture
def template_render(mocker):
    mock_get_template = MagicMock()
    mock_render = MagicMock()
    mock_get_template.render = mock_render
    mocker.patch('jupyterhub_admin.apps.images.views.loader.get_template', return_value=mock_get_template)
    yield mock_render


def test_index(authenticated_client, template_render, get_config_metadata, metadata):
    context = {
        'error': False,
        'images': metadata['value']['images']
    }
    response = authenticated_client.get('/images/')
    template_render.assert_called_with(context, ANY)


def test_images(authenticated_client, template_render, get_config_metadata, metadata):
    context = {
        'error': False,
        'index': 1,
        'header': "JupyterHub Image Configuration",
        'fields': [
            {
                'label': 'Display Name',
                'id': 'display_name',
                'value': 'Image 1',
                'type': 'text',
                'placeholder': 'Name of the image to display in the spawner'
            },
            {
                'label': 'Image Name',
                'id': 'image_name',
                'value': 'org/repo1:tag',
                'type': 'text',
                'placeholder': 'Image repository, name and tag'
            }
        ],
        'message': 'Configuration for Image 1',
        'api': '/images/api/1',
        'delete_confirmation': 'Image 1 (org/repo1:tag)'
    }
    response = authenticated_client.get('/images/1')
    template_render.assert_called_with(context, ANY)


def test_api_post(authenticated_client, get_config_metadata, write_config_metadata, metadata):
    data = {
        'display_name': 'Image 2',
        'name': 'org/repo2:tag'
    }
    expected = metadata['value'].copy()
    expected['images'][1] = data
    response = authenticated_client.post('/images/api/1', data=data)
    assert response.status_code == 200
    write_config_metadata.assert_called_with(expected)


def test_api_new(authenticated_client, get_config_metadata, write_config_metadata, metadata):
    data = {
        'display_name': 'Image 2',
        'name': 'org/repo2:tag'
    }
    expected = metadata['value'].copy()
    expected['images'].append(data)
    response = authenticated_client.post('/images/api/new', data=data)
    assert response.status_code == 200
    write_config_metadata.assert_called_with(expected)


def test_api_delete(authenticated_client, get_config_metadata, write_config_metadata, metadata):
    response = authenticated_client.delete('/images/api/1')
    assert response.status_code == 200
    write_config_metadata.assert_called_with({'images': [{'display_name': 'Image 0', 'name': 'org/repo0:tag'}]})
