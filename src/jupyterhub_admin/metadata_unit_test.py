from jupyterhub_admin.metadata import get_config_metadata_name


def test_get_config_metadata_name():
    assert get_config_metadata_name() == "config.JUPYTERHUB_NAME.jhub"