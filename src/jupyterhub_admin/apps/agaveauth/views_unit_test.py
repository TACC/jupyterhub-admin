from django.conf import settings
import pytest
from django.urls import reverse


TEST_STATE = "ABCDEFG123456"

pytestmark = pytest.mark.django_db


@pytest.fixture
def regular_user(django_user_model, django_db_reset_sequences):
    django_user_model.objects.create_user(username="username",
                                          password="password",
                                          first_name="Firstname",
                                          last_name="Lastname",
                                          email="user@user.com")
    user = django_user_model.objects.get(username="username")
    user.save()
    yield user


def test_auth_agave(client, mocker):
    mocker.patch(
        'jupyterhub_admin.apps.agaveauth.views._get_auth_state',
        return_value=TEST_STATE
    )

    response = client.get("/auth/agave", follow=False)

    agave_authorize = \
        "{}/authorize?client_id=AGAVE_CLIENT_KEY&response_type=code&redirect_uri=https://testserver/auth/agave/callback&state={}".format(
            settings.AGAVE_API, TEST_STATE
        )

    assert response.status_code == 302
    assert response.url == agave_authorize
    assert client.session['auth_state'] == TEST_STATE


def test_agave_callback(client, mocker, regular_user):
    mock_authenticate = mocker.patch('jupyterhub_admin.apps.agaveauth.views.authenticate')
    mock_agave_token_post = mocker.patch('jupyterhub_admin.apps.agaveauth.views.requests.post')

    # add auth to session
    session = client.session
    session['auth_state'] = TEST_STATE
    session.save()

    mock_agave_token_post.return_value.json.return_value = {
        "token_type": "bearer",
        "scope": "default",
        "access_token": "4c8728a095934e10a642ad8371fcbe",
        "expires_in": 12457,
        "refresh_token": "d6ede1effb7be9c3efd7feba5f5af6"
    }
    mock_agave_token_post.return_value.status_code = 200
    mock_authenticate.return_value = regular_user

    response = client.get("/auth/agave/callback?state={}&code=83163624a0bc41c4a376e0acb16a62f9".format(TEST_STATE))
    assert response.status_code == 302
    assert response.url == settings.LOGIN_REDIRECT_URL


def test_agave_callback_no_code(client):
    # add auth to session
    session = client.session
    session['auth_state'] = TEST_STATE
    session.save()

    response = client.get("/auth/agave/callback?state={}".format(TEST_STATE))
    assert response.status_code == 302
    assert response.url == reverse('auth:logout')


def test_agave_callback_mismatched_state(client):
    # add auth to session
    session = client.session
    session['auth_state'] = "TEST_STATE"
    session.save()
    response = client.get("/auth/agave/callback?state={}".format('bar'))
    assert response.status_code == 400
