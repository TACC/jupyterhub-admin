import pytest


@pytest.fixture
def mock_agave_client(mocker):
    yield mocker.patch('portal.apps.auth.models.AgaveOAuthToken.client', autospec=True)


@pytest.fixture
def mock_environment(monkeypatch, variables):
    def mock_get(variable, default):
        if var == 'DJANGO_SECRET_KEY':
            return 'MOCK_DJANGO_SECRET_KEY'
        elif var == 'JUPYTERHUB_TOKEN':
            return 'MOCK_JUPYTERHUB_TOKEN'
        elif var == 'JUPYTERHUB_API':
            return 'MOCK_JUPYTERHUB_API'
        return default
    monkeypatch.setattr(os.environ, 'get', mock_get)