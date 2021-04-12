import pytest


def test_settings(settings):
    #from django.conf import settings
    assert settings.JUPYTERHUB_TOKEN is not None