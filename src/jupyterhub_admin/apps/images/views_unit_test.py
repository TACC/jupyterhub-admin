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


def test_index(client, template_render, get_config_metadata, metadata):
    context = {
        'error': False,
        'images': metadata['value']['images']
    }
    response = client.get('/images/')
    template_render.assert_called_with(context, ANY)


def test_image(client, template_render, get_config_metadata, metadata):
    context = {
        'error': False,
        'index': 1,
        'image': metadata['value']['images'][1],
        'message': "Configuration for Image 1"
    }
    response = client.get('/images/1')
    template_render.assert_called_with(context, ANY)
