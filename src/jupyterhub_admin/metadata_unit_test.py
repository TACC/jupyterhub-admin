import pytest
from jupyterhub_admin.metadata import (
    get_config_metadata_name,
    get_config_metadata,
    write_config_metadata,
    set_config,
    get_group_config_metadata,
    list_group_config_metadata,
    write_group_config_metadata,
    get_group_config_metadata_name
)


@pytest.fixture
def mock_agave(mocker):
    yield mocker.patch('jupyterhub_admin.metadata.get_agave_client', autouse=True)


def test_get_config_metadata_name():
    assert get_config_metadata_name() == "config.JUPYTERHUB.PROD.jhub"


def test_get_config_metadata(mock_agave):
    mock_agave.return_value.meta.listMetadata.return_value = [
        {
            'name': 'config.JUPYTERHUB.PROD.jhub',
            'value': 'MOCK_VALUE'
        }
    ]
    assert get_config_metadata()['value'] == 'MOCK_VALUE'


def test_write_config_metadata(mocker, mock_agave):
    mocker.patch('jupyterhub_admin.metadata.get_config_metadata', return_value={
        'uuid': 'MOCK_UUID'  
    })
    write_config_metadata({ 'key': 'value' })
    mock_agave.return_value.meta.updateMetadata.assert_called_with(
        body={'uuid': 'MOCK_UUID', 'value': {'key': 'value'}},
        uuid='MOCK_UUID'
    )


def test_set_config_existing(mocker):
    mocker.patch('jupyterhub_admin.metadata.get_config_metadata', return_value={
        'value': {
            'key1': 'value1'
        }
    })
    mock_write = mocker.patch('jupyterhub_admin.metadata.write_config_metadata')
    set_config('key1', 'value1_changed')
    mock_write.assert_called_with({ 'key1': 'value1_changed' })


def test_set_config_new(mocker):
    mocker.patch('jupyterhub_admin.metadata.get_config_metadata', return_value={
        'value': {
            'key1': 'value1'
        }
    })
    mock_write = mocker.patch('jupyterhub_admin.metadata.write_config_metadata')
    set_config('key2', 'value2')
    mock_write.assert_called_with({ 'key1': 'value1', 'key2': 'value2' })


def test_get_group_config_metadata_name():
    assert get_group_config_metadata_name("MYGROUP") == "MYGROUP.group.config.JUPYTERHUB.PROD.jhub"


def test_get_group_config_metadata(mock_agave):
    mock_agave.return_value.meta.listMetadata.return_value = [
        {
            'name': 'MYGROUP.group.config.JUPYTERHUB.PROD.jhub',
            'value': 'MOCK_VALUE'
        }
    ]
    assert get_group_config_metadata("MYGROUP")['value'] == 'MOCK_VALUE'
    mock_agave.return_value.meta.listMetadata.assert_called_with(
        q='{"name": "MYGROUP.group.config.JUPYTERHUB.PROD.jhub"}'
    )


def test_list_group_config_metadata(mock_agave):
    mock_agave.return_value.meta.listMetadata.return_value = [
        {
            'name': 'MYGROUP.group.config.JUPYTERHUB.PROD.jhub',
            'value': 'MOCK_VALUE'
        }
    ]
    assert list_group_config_metadata()[0]['value'] == 'MOCK_VALUE'
    mock_agave.return_value.meta.listMetadata.assert_called_with(
        q='{"name": {"$regex": ".*group.config.JUPYTERHUB.PROD.jhub"}}'
    )


def test_write_group_config_metadata(mocker, mock_agave):
    mock_meta_get = mocker.patch('jupyterhub_admin.metadata.get_group_config_metadata', return_value={
        'uuid': 'MOCK_UUID'  
    })
    write_group_config_metadata("MYGROUP", { 'key': 'value' })
    mock_meta_get.assert_called_with("MYGROUP")
    mock_agave.return_value.meta.updateMetadata.assert_called_with(
        body={'uuid': 'MOCK_UUID', 'value': {'key': 'value'}},
        uuid='MOCK_UUID'
    )
