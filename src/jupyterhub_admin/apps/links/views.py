from django.shortcuts import render
from django.template import loader
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from jupyterhub_admin.metadata import get_admin_tenant_metadata
import logging

logger = logging.getLogger(__name__)

# Create your views here.
@login_required
def index(request):
    template = loader.get_template("links/index.html")
    context = {
        'error': False,
        'links': []
    }
    try:
        metadata = get_admin_tenant_metadata()
        links = []
        for entry in metadata:
            if 'admin_users' in entry['value'] and settings.TENANT in entry['value']['admin_users']:
                context['links'].append({
                    'link': entry['value']['oauth_callback_url'].removesuffix('/hub/oauth_callback')
                })
    except Exception as e:
        context['error'] = True
        context['message'] = 'Admin links could not be retrieved'
        logger.exception(e)
    return HttpResponse(template.render(context, request))
