import pytest


@pytest.fixture
def mock_agave_client(mocker):
    yield mocker.patch('portal.apps.auth.models.AgaveOAuthToken.client', autospec=True)