from agavepy import Agave
from django.conf import settings
import json


def get_config_metadata_name():
    return f"config.{settings.TENANT}.{settings.INSTANCE}.jhub"


def get_config_metadata():
    ag = Agave(api_server=settings.AGAVE_API, token=settings.AGAVE_SERVICE_TOKEN)
    metadata = ag.meta.listMetadata()
    matching = list(filter(
        lambda meta: meta['name'] == get_config_metadata_name(),
        metadata
    ))
    return matching[0]


def write_config_metadata(value):
    ag = Agave(api_server=settings.AGAVE_API, token=settings.AGAVE_SERVICE_TOKEN)
    meta = get_config_metadata()
    meta['value'] = value
    ag.meta.updateMetadata(body=meta, uuid=meta['uuid'])


def set_config(key, value):
    current = get_config_metadata()['value']
    current[key] = value
    write_config_metadata(current)