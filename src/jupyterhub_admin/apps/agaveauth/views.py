"""
Auth views.
"""
import logging
import time
import requests
import secrets
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render


logger = logging.getLogger(__name__)
METRICS = logging.getLogger('metrics.{}'.format(__name__))


def logged_out(request):
    return render(request, 'auth/logged_out.html')


def _get_auth_state():
    return secrets.token_hex(24)


def _get_redirect_uri(request):
    redirect_uri = 'https://{}{}'
    if request.get_host() == "localhost:8000":
        redirect_uri = 'http://{}{}'
    redirect_uri = redirect_uri.format(
        request.get_host(),
        reverse('auth:agave_oauth_callback')
    )
    return redirect_uri


# Create your views here.
def agave_oauth(request):
    """First step for agave OAuth workflow.
    """
    tenant_base_url = getattr(settings, 'AGAVE_API')
    client_key = getattr(settings, 'AGAVE_CLIENT_KEY')

    session = request.session
    session['auth_state'] = _get_auth_state()
    next_page = request.GET.get('next')
    if next_page:
        session['next'] = next_page
    redirect_uri = _get_redirect_uri(request)
    METRICS.debug("user:{} starting oauth redirect login".format(request.user.username))
    authorization_url = (
        '%s/authorize?client_id=%s&response_type=code&redirect_uri=%s&state=%s' % (
            tenant_base_url,
            client_key,
            redirect_uri,
            session['auth_state'],
        )
    )
    return HttpResponseRedirect(authorization_url)


def agave_oauth_callback(request):
    """Agave OAuth callback handler.
    """

    state = request.GET.get('state')

    if request.session['auth_state'] != state:
        msg = ('OAuth Authorization State mismatch!? auth_state=%s '
               'does not match returned state=%s' % (request.session['auth_state'], state))
        logger.warning(msg)
        return HttpResponseBadRequest('Authorization State Failed')

    if 'code' in request.GET:
        redirect_uri = _get_redirect_uri(request)
        logger.debug('redirect_uri %s', redirect_uri)
        code = request.GET['code']
        tenant_base_url = getattr(settings, 'AGAVE_API')
        client_key = getattr(settings, 'AGAVE_CLIENT_KEY')
        client_sec = getattr(settings, 'AGAVE_CLIENT_SECRET')
        body = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
        }
        # TODO update to token call in agavepy
        logger.debug("Redeem authorization code for token")
        response = requests.post('%s/token' % tenant_base_url,
                                 data=body,
                                 auth=(client_key, client_sec))
        token_data = response.json()
        logger.debug(token_data)
        token_data['created'] = int(time.time())
        # log user in
        user = authenticate(backend='agave', token=token_data['access_token'])

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
