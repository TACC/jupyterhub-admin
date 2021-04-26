from jupyterhub_admin.metadata import get_config_metadata


def test_get_config_metadata():
    assert get_config_metadata()['value']['config_type'] == 'tenant'