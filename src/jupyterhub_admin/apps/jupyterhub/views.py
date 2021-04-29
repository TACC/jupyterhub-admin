from django.http import HttpResponse
from django.template import loader
from jupyterhub_admin.jhub_api import get_users
import dateutil.parser
import logging


logger = logging.getLogger(__name__)


def index(request):
    timeformat = '%Y-%m-%d %H:%M'
    template = loader.get_template("jupyterhub/index.html")
    context = {
        'error': False,
        'servers': []
    }
    try:
        users = get_users()
        for user in users:
            servers = list(user['servers'].items())
            if len(servers) > 0:
                server = servers[0][1]
                context['servers'].append({
                    'username': user['name'],
                    'started':  dateutil.parser.isoparse(server['started']).strftime(timeformat),
                    'last_activity':  dateutil.parser.isoparse(server['last_activity']).strftime(timeformat)
                })
    except Exception as e:
        context['error'] = True
        logger.exception()
    return HttpResponse(template.render(context, request))