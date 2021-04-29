from django.http import HttpResponse
from django.template import loader
from jupyterhub_admin.jhub_api import (
    get_users,
    get_user,
    parse_user,
    has_server
)
import dateutil.parser
import logging


logger = logging.getLogger(__name__)


def format_user(user):
    timeformat = '%Y-%m-%d %H:%M'
    if user['server'] is not None:
        user['server']['started'] = dateutil.parser.isoparse(user['server']['started']).strftime(timeformat)
        user['server']['last_activity'] = dateutil.parser.isoparse(user['server']['last_activity']).strftime(timeformat)
    return user


def apply_sorting(users, sorting=None):
    users = sorted(users, key=lambda user: user['name'])
    if sorting:
        active_users = [ user for user in users if user['server'] ]
        inactive_users = [ user for user in users if not user['server'] ]
        if sorting == 'started':
            active_users = sorted(
                active_users,
                key=lambda user: dateutil.parser.isoparse(user['server']['started']),
                reverse=True
            )
        elif sorting == 'last_activity':
            active_users = sorted(
                active_users,
                key=lambda user: dateutil.parser.isoparse(user['server']['last_activity']),
                reverse=True
            )
        users = active_users + inactive_users
    return users


def index(request):
    template = loader.get_template("jupyterhub/index.html")
    sorting = request.GET.get('sorting', None)
    context = {
        'error': False,
        'sorting': sorting,
        'users': []
    }
    try:
        users = [ parse_user(user) for user in get_users() ]
        users = apply_sorting(users, sorting)
        context['users'] = [ format_user(user) for user in users ]
    except Exception as e:
        context['error'] = True
        logger.exception()
    return HttpResponse(template.render(context, request))


def user(request, username):
    template = loader.get_template("jupyterhub/user.html")
    context = {
        'error': False,
        'username': username
    }
    try:
        contexet['user'] = user_context(parse_user(get_user(username)))
    except Exception as e:
        context['error'] = True
        logger.exception()
    return HttpResponse(username)