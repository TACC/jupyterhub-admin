import pytest


@pytest.fixture
def authenticated_client(django_user_model, client):
    django_user_model.objects.create_user(username="username",
                                          password="password",
                                          first_name="Firstname",
                                          last_name="Lastname",
                                          email="user@user.com")
    user = django_user_model.objects.get(username="username")
    client.force_login(user)
    yield client