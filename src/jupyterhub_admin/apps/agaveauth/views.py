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


logger = logging.getLogger(__name__)
METRICS = logging.getLogger('metrics.{}'.format(__name__))


def logged_out(request):
    logout(request)
    return render(request, 'auth/logged_out.html')


def _get_auth_state():
    return secrets.token_hex(24)


def _get_redirect_uri(request):
    logger.debug("AgaveOauth Request")
    logger.debug("METADATA:")
    logger.debug(request.META)
    redirect_uri = 'https://{}{}'
    if request.get_host() == "localhost:8000":
        redirect_uri = 'http://{}{}'
    redirect_uri = redirect_uri.format(
        request.get_host(),
        reverse('auth:agave_oauth_callback')
    )
    logger.debug(redirect_uri)
    return redirect_uri


# Create your views here.
def agave_oauth(request):
    """First step for Tapis OAuth workflow.
    """
    tenant_base_url = getattr(settings, 'TAPIS_API')
    client_id = getattr(settings, 'TAPIS_CLIENT_KEY')
    client_key = getattr(settings, 'TAPIS_CLIENT_SECRET')
    token = getattr(settings, 'TAPIS_SERVICE_TOKEN')
    session = request.session
    session['auth_state'] = _get_auth_state()
    next_page = request.GET.get('next')
    if next_page:
        session['next'] = next_page
    redirect_uri = _get_redirect_uri(request)

    METRICS.debug(request.user)
    METRICS.debug(request.GET.get('state'))

    METRICS.debug("user:{} starting oauth redirect login".format(request.user.username))
    authorization_url = (
        '%s/oauth2/authorize?client_id=%s&redirect_uri=%s&response_type=code&state=%s' % (
            tenant_base_url,
            client_id,
            redirect_uri,
            session['auth_state'],
        )
    )
    logger.debug(authorization_url)
    return HttpResponseRedirect(authorization_url)


def agave_oauth_callback(request):
    """Tapis OAuth callback handler.
    """
    logger.debug("Agave OAuth callback")

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
        client_id=getattr(settings, 'TAPIS_CLIENT_KEY')
        client_secret=getattr(settings, 'TAPIS_CLIENT_SECRET')

        credentials = client_id + ":" + client_secret
        cred_bytes = credentials.encode('ascii')
        cred_base64 = base64.b64encode(cred_bytes)

        body = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
        }
        # TODO update to token call in agavepy
        METRICS.debug("Redeem authorization code for token")
        response = requests.post('%s/oauth2/tokens' % tenant_base_url,
                                 data=body,
                                 auth=credentials)
        token_data = response.json()
        logger.debug(token_data)
        token_data['created'] = int(time.time())
        # log user in
        #user = authenticate(backend='agave', token=token_data['access_token'])

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

    if 'next' in request.session:
        next_uri = request.session.pop('next')
        return HttpResponseRedirect(next_uri)
    else:
        login_url = getattr(settings, 'LOGIN_REDIRECT_URL')
        return HttpResponseRedirect(reverse('main:index'))


def agave_session_error(request):
    """Agave token error handler.
    """
    pass
