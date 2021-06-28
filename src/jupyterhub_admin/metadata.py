from agavepy import Agave
from django.conf import settings
import json


def get_config_metadata_name():
    return f"config.{settings.TENANT}.{settings.INSTANCE}.jhub"


def get_group_config_metadata_name(group):
    return f"{group}.group.{get_config_metadata_name()}"


def get_agave_client():
    return Agave(api_server=settings.AGAVE_API, token=settings.AGAVE_SERVICE_TOKEN)


def get_config_metadata():
    ag = get_agave_client()
    query = {'name':get_config_metadata_name()}
    metadata = ag.meta.listMetadata(q=json.dumps(query))
    return metadata[0]


def list_group_config_metadata():
    ag = get_agave_client()
    query = { 'name': {'$regex': f".*group.{get_config_metadata_name()}"}}
    metadata = ag.meta.listMetadata(q=json.dumps(query))
    return metadata


def get_group_config_metadata(group):
    ag = get_agave_client()
    query = {'name': get_group_config_metadata_name(group)}
    metadata = ag.meta.listMetadata(q=json.dumps(query))
    return metadata[0]


def write_group_config_metadata(group, value):
    ag = get_agave_client()
    meta = get_group_config_metadata(group)
    meta['value'] = value
    ag.meta.updateMetadata(body=meta, uuid=meta['uuid'])


def new_group_config(group):
    ag = get_agave_client()
    meta = {
        "name": get_group_config_metadata_name(group),
        "value": {
            "tenant": settings.TENANT,
            "instance": settings.INSTANCE,
            "user": [],
            "images": [],
            "config_type": "group",
            "volume_mounts": [],
            "group_name": group,
            "name": get_group_config_metadata_name(group)
        }
    }
    ag.meta.addMetadata(body=meta)


def write_config_metadata(value):
    ag = get_agave_client()
    meta = get_config_metadata()
    meta['value'] = value
    ag.meta.updateMetadata(body=meta, uuid=meta['uuid'])


def set_config(key, value):
    current = get_config_metadata()['value']
    current[key] = value
    write_config_metadata(current)