from django.conf import settings
import requests


def jupyterhub_request(method, endpoint, data=None, params=None):
    api_url = settings.JUPYTERHUB_API + endpoint
    headers = {
        'Authorization': 'token %s' % settings.JUPYTERHUB_TOKEN
    }
    if method == 'POST':
        return requests.post(api_url, data=data)
    elif method == 'GET':
        return requests.get(api_url, params=params)
    elif method == 'DELETE':
        return requests.get(api_url, params=params)


def get_version():
    return jupyterhub_request('GET', '/').json()
