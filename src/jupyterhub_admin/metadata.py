from agavepy import Agave
from django.conf import settings
import json


def get_config_metadata_name():
    return f"config.{settings.JUPYTERHUB_NAME}.jhub"


def get_config_metadata():
    ag = Agave(api_server=settings.AGAVE_API, token=settings.AGAVE_TOKEN)
    metadata = ag.meta.listMetadata()
    matching = list(filter(
        lambda meta: meta['name'] == get_config_metadata_name(),
        metadata
    ))
    return matching[0]


def write_config_metadata(value):
    ag = Agave(api_server=settings.AGAVE_API, token=settings.AGAVE_TOKEN)
    original = get_config_metadata()
    ag.meta.updateMetadata(body=json.dumps(value), uuid=original['uuid'])


def set_config(key, value):
    current = get_config_metadata()['value']
    current[key] = value
    write_config_metadata(current)