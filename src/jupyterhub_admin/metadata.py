from agavepy import Agave
from django.conf import settings


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
