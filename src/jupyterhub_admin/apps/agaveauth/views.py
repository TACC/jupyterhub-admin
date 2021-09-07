"""
Auth views.
"""
import logging
import time
import requests
import secrets
import base64
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from requests.auth import HTTPBasicAuth
from tapipy.tapis import Tapis


logger = logging.getLogger(__name__)
METRICS = logging.getLogger('metrics.{}'.format(__name__))


def logged_out(request):
    logout(request)
    return render(request, 'auth/logged_out.html')


def _get_auth_state():
    return secrets.token_hex(24)


def _get_redirect_uri(request):
    redirect_uri = 'https://{}{}'
    if request.get_host() == "localhost:8000":
        redirect_uri = 'http://{}{}'
    redirect_uri = redirect_uri.format(
        request.get_host(),
        reverse('auth:tapis_oauth_callback')
    )
    return redirect_uri


# Create your views here.
def tapis_oauth(request):
    """First step for Tapis OAuth workflow.
    """
    tenant_base_url = getattr(settings, 'TAPIS_API')
    client_id = getattr(settings, 'TAPIS_CLIENT_ID')
    client_key = getattr(settings, 'TAPIS_CLIENT_KEY')
    token = getattr(settings, 'TAPIS_SERVICE_TOKEN')

    session = request.session
    session['auth_state'] = _get_auth_state()
    next_page = request.GET.get('next')
    if next_page:
        session['next'] = next_page
    redirect_uri = _get_redirect_uri(request)

    METRICS.debug("user:{} starting oauth redirect login".format(request.user.username))

    authorization_url = (
        '%s/oauth2/authorize?client_id=%s&redirect_uri=%s&response_type=code&state=%s' % (
            tenant_base_url,
            client_id,
            redirect_uri,
            session['auth_state'],
        )
    )
    return HttpResponseRedirect(authorization_url)


def tapis_oauth_callback(request):
    """Tapis OAuth callback handler.
    """
    state = request.GET.get('state')

    if request.session['auth_state'] != state:
        msg = ('OAuth Authorization State mismatch!? auth_state=%s '
               'does not match returned state=%s' % (request.session['auth_state'], state))
        logger.warning(msg)
        return HttpResponseBadRequest('Authorization State Failed')

    if 'code' in request.GET:
        redirect_uri = _get_redirect_uri(request)
        METRICS.debug('redirect_uri %s', redirect_uri)

        code = request.GET['code']
        tenant_base_url = getattr(settings, 'TAPIS_API')
        tenant_base_url = "https://jupyter-tacc-dev.tapis.io"
        tapis_user = getattr(settings, 'TAPIS_USER')
        tapis_pass = getattr(settings, 'TAPIS_PASS')

        t = Tapis(base_url=tenant_base_url,
                  username=tapis_user,
                  password=tapis_pass)
        t.get_tokens()

        token = t.access_token.access_token

        # log user in
        user = authenticate(backend='tapis', t=t)

        if user:
            login(request, user)
            METRICS.debug("user:{} successful oauth login".format(user.username))
        else:
            messages.error(
                request,
                'Authentication failed. Please try again. If this problem '
                'persists please submit a support ticket.'
            )
            return HttpResponseRedirect(reverse('auth:logout'))
    else:
        if 'error' in request.GET:
            error = request.GET['error']
            logger.warning('Authorization failed: %s', error)

        return HttpResponseRedirect(reverse('auth:logout'))

    if 'v3_next' in request.session:
        next_uri = request.session.pop('v3_next')
        return HttpResponseRedirect(next_uri)
    else:
        login_url = getattr(settings, 'LOGIN_REDIRECT_URL')
        return HttpResponseRedirect(reverse('main:index'))


def tapis_session_error(request):
    """Tapis token error handler.
    """
    pass
