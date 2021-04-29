import pytest
from jupyterhub_admin.jhub_api import (
    parse_user,
    has_server
)


@pytest.fixture
def test_user():
    yield {
        'kind': 'user',
        'name': 'jchuah',
        'admin': False,
        'groups': [],
        'server': '/user/jchuah/',
        'pending': None,
        'created': '2021-04-22T15:59:25.298461Z',
        'last_activity': '2021-04-22T18:56:53.630049Z',
        'servers': {
            '': {
                'name': '',
                'last_activity': '2021-04-22T18:56:53.630049Z',
                'started': '2021-04-22T15:59:29.685793Z',
                'pending': None,
                'ready': True,
                'state': {
                    'pod_name': 'jupyter-jchuah'
                },
                'url': '/user/jchuah/',
                'user_options': {},
                'progress_url': '/hub/api/users/jchuah/server/progress'
            }
        }
    }


def test_has_server(test_user):
    assert has_server(test_user)
    del test_user['servers']['']
    assert not has_server(test_user)
    del test_user['servers']
    assert not has_server(test_user)


def test_parse_user(test_user):
    result = parse_user(test_user)
    assert result['server']['url'] == '/user/jchuah/'