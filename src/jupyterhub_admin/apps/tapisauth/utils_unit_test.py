import pytest
from jupyterhub_admin.apps.tapisauth.utils import add_admin_user, remove_admin_user



@pytest.fixture
def write_meta(mocker):
    yield mocker.patch('jupyterhub_admin.apps.tapisauth.utils.write_config_metadata')


@pytest.fixture
def get_meta(mocker):
    yield mocker.patch('jupyterhub_admin.apps.tapisauth.utils.get_config_metadata')


def test_no_admin_users(get_meta, write_meta):
    get_meta.return_value = {
        'value': {
        }
    }
    add_admin_user('username')
    write_meta.assert_called_with({
        'admin_users': ['username']
    })


def test_add_admin(get_meta, write_meta):
    get_meta.return_value = {
        'value': {
            'admin_users': []
        }
    }
    add_admin_user('username')
    write_meta.assert_called_with({
        'admin_users': ['username']
    })


def test_admin_exists(get_meta, write_meta):
    get_meta.return_value = {
        'value': {
            'admin_users': ['username']
        }
    }
    with pytest.raises(Exception):
        add_admin_user('username')
    write_meta.assert_not_called()


def test_remove_admin(get_meta, write_meta):
    get_meta.return_value = {
        'value': {
            'admin_users': ['username']
        }
    }
    remove_admin_user('username')
    write_meta.assert_called_with({
        'admin_users': []
    })


def test_remove_admin_no_list(get_meta, write_meta):
    get_meta.return_value = {
        'value': {}
    }
    with pytest.raises(Exception):
        remove_admin_user('username')
    write_meta.assert_not_called()


def test_remove_admin_does_not_exist(get_meta, write_meta):
    get_meta.return_value = {
        'value': {
            'admin_users': []
        }
    }
    with pytest.raises(Exception):
        remove_admin_user('username')
    write_meta.assert_not_called()
