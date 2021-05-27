import pytest
from jupyterhub_admin.apps.agaveauth.backends import AgaveOAuthBackend


pytestmark = pytest.mark.django_db


@pytest.fixture
def profile_mock(mocker):
    yield mocker.patch('jupyterhub_admin.apps.agaveauth.backends.requests.get')


@pytest.fixture
def metadata_mock(mocker):
    yield mocker.patch('jupyterhub_admin.apps.agaveauth.backends.get_config_metadata')

def test_not_agave_backend():
    backend = AgaveOAuthBackend()
    assert backend.authenticate() is None
    assert backend.authenticate(backend='notagave') is None


def test_no_profile(profile_mock):
    backend = AgaveOAuthBackend()
    profile_mock.return_value.json.return_value = {
    }
    assert backend.authenticate() is None
    profile_mock.return_value.json.return_value = {
        'status': 'failure'
    }
    assert backend.authenticate(backend='agave', token='mock_token') is None



def test_user_not_in_metadata(profile_mock, metadata_mock):
    backend = AgaveOAuthBackend()
    profile_mock.return_value.json.return_value = {
        'status': 'success',
        'result': {
            'username': 'username'
        }
    }
    metadata_mock.return_value = {
    }
    assert backend.authenticate(backend='agave', token='mock_token') is None
    metadata_mock.return_value = {
        'admin_users': []
    }
    assert backend.authenticate(backend='agave', token='mock_token') is None


def test_authenticate(profile_mock, metadata_mock):
    backend = AgaveOAuthBackend()
    profile_mock.return_value.json.return_value = {
        'status': 'success',
        'result': {
            'username': 'username'
        }
    }
    metadata_mock.return_value = {
        'admin_users': ['username']
    }
    assert backend.authenticate(backend='agave', token='mock_token').username == 'username'