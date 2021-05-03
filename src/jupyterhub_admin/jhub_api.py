from django.conf import settings
import requests
import logging

def jupyterhub_request(method, endpoint, data=None, params=None):
    api_url = settings.JUPYTERHUB_API + endpoint
    headers = {
        'Authorization': 'token %s' % settings.JUPYTERHUB_TOKEN
    }
    print("API_URL", api_url)
    if method == 'POST':
        return requests.post(api_url, data=data, headers=headers)
    elif method == 'GET':
        return requests.get(api_url, params=params, headers=headers)
    elif method == 'DELETE':
        return requests.delete(api_url, params=params, headers=headers)


def get_version():
    return jupyterhub_request('GET', '/').json()


def get_users():
    return jupyterhub_request('GET', '/users').json()


def get_user(username):
    return jupyterhub_request('GET', f'/users/{username}').json()


def stop_server(username):
    return jupyterhub_request('DELETE', f'/users/{username}/server')


def parse_user(user):
    """
    Parse a user object and dereference its server dictionary
    """
    result = user.copy()
    result['server'] = None
    del result['servers']
    if has_server(user):
        result['server'] = list(user['servers'].items())[0][1]
    return result


def has_server(user):
    """
    True if a user has an active server
    """
    try:
        return len(list(user['servers'].items())) > 0
    except:
        return False