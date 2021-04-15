from jupyterhub_admin.jhub_api import get_version


def test_get_version():
    assert "version" in get_version()