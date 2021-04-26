from jupyterhub_admin.jhub_api import get_version, get_users


def test_get_version():
    assert "version" in get_version()


def test_get_users():
    assert isinstance(get_users(), list)