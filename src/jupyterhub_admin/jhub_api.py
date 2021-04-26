from django.conf import settings
import requests
import logging

def jupyterhub_request(method, endpoint, data=None, params=None):
    api_url = settings.JUPYTERHUB_API + endpoint
    headers = {
        'Authorization': 'token %s' % settings.JUPYTERHUB_TOKEN
    }
    print(api_url)
    print(headers)
    if method == 'POST':
        return requests.post(api_url, data=data, headers=headers)
    elif method == 'GET':
        return requests.get(api_url, params=params, headers=headers)
    elif method == 'DELETE':
        return requests.get(api_url, params=params, headers=headers)


def get_version():
    return jupyterhub_request('GET', '/').json()


def get_users():
    return jupyterhub_request('GET', '/users').json()
