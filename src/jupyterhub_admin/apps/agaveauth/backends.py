"""Auth backends"""
import logging
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from jupyterhub_admin.metadata import get_config_metadata
import jwt

#pylint: disable=invalid-name
logger = logging.getLogger(__name__)
#pylint: enable=invalid-name

class AgaveOAuthBackend(ModelBackend):
    def authenticate(self, *args, **kwargs):
        user = None
        try:
            if 'backend' not in kwargs or kwargs['backend'] != 'tapis':
                raise Exception('Skipping AgaveOAuthBackend')
            token = kwargs['token']
            logger.debug(token)
            base_url = getattr(settings, 'TAPIS_API')

            #tenant_res = requests.get("https://admin.tapis.io/v3/tenants/jupyter-tacc-dev")
            #tenant_json = tenant_res.json()
            #pub_key = tenant_json['result']['public_key']

            #decoded_jwt = jwt.decode(token, pub_key, algorithms=["RS256"])

            logger.info('Attempting login via Tapis with token "%s"' %
                            token[:8].ljust(len(token), '-'))

            #logger.debug(decoded_jwt)
            #username = decoded_jwt['tapis/username']
            response = requests.get('%s/oauth2/profiles/me' % (base_url),
                                    headers={'Authorization': 'Bearer %s' % token})

            logger.debug("response %s" % response)
            json_result = response.json()
            logger.debug(json_result)
            
            if 'status' not in json_result or json_result['status'] != 'success':
                raise Exception('Agave Authentication failed: %s' % json_result)
            agave_user = json_result['result']
            username = agave_user['username']
            meta = get_config_metadata()
            if 'admin_users' not in meta['value'] or username not in meta['value']['admin_users']:
                raise Exception('%s is not a hub admin user' % username)
            UserModel = get_user_model()
            user, _ = UserModel.objects.get_or_create(username=username)
            user.save()
            logger.info('Login successful for user "%s"' % username)
        except Exception as e:
            logger.exception(e)
        return user
