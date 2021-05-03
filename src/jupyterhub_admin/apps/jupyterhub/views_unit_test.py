import pytest
from jupyterhub_admin.apps.jupyterhub.views import apply_sorting


@pytest.fixture
def test_users():
    yield [
        {
            'name': 'c_user',
            'server': {
                'last_activity': '2021-04-22T00:00:00.000000Z',
                'started': '2021-04-23T00:00:00.000000Z',
            }
        },
        {
            'name': 'a_user',
            'server': {
                'last_activity': '2021-04-23T00:00:00.000000Z',
                'started': '2021-04-22T00:00:00.000000Z',
            }
        },
        {
            'name': 'b_user',
            'server': None
        }
    ]


def test_apply_sorting(test_users):
    result = apply_sorting(test_users)
    assert result[0]['name'] == 'a_user'
    assert result[1]['name'] == 'b_user'
    assert result[2]['name'] == 'c_user'
    result = apply_sorting(test_users, sorting='started')
    assert result[0]['name'] == 'c_user'
    assert result[1]['name'] == 'a_user'
    assert result[2]['name'] == 'b_user'
    result = apply_sorting(test_users, sorting='last_activity')
    assert result[0]['name'] == 'a_user'
    assert result[1]['name'] == 'c_user'
    assert result[2]['name'] == 'b_user'