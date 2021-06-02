"""Auth backends"""
import logging
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from jupyterhub_admin.metadata import get_config_metadata

#pylint: disable=invalid-name
logger = logging.getLogger(__name__)
#pylint: enable=invalid-name

class AgaveOAuthBackend(ModelBackend):
    def authenticate(self, *args, **kwargs):
        user = None
        try:
            if 'backend' not in kwargs or kwargs['backend'] != 'agave':
                raise Exception('Skipping AgaveOAuthBackend')
            token = kwargs['token']
            base_url = getattr(settings, 'AGAVE_API')

            logger.info('Attempting login via Agave with token "%s"' %
                            token[:8].ljust(len(token), '-'))
            response = requests.get('%s/profiles/v2/me' % base_url,
                                    headers={'Authorization': 'Bearer %s' % token})
            json_result = response.json()
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
