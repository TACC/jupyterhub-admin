"""Auth backends"""
import logging
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

#pylint: disable=invalid-name
logger = logging.getLogger(__name__)
#pylint: enable=invalid-name

class AgaveOAuthBackend(ModelBackend):

    def authenticate(self, *args, **kwargs):
        user = None

        if 'backend' in kwargs and kwargs['backend'] == 'agave':
            token = kwargs['token']
            base_url = getattr(settings, 'AGAVE_API')

            logger.info('Attempting login via Agave with token "%s"' %
                             token[:8].ljust(len(token), '-'))
            response = requests.get('%s/profiles/v2/me' % base_url,
                                    headers={'Authorization': 'Bearer %s' % token})
            json_result = response.json()
            if 'status' in json_result and json_result['status'] == 'success':
                agave_user = json_result['result']
                username = agave_user['username']
                UserModel = get_user_model()
                user, _ = UserModel.objects.get_or_create(username=username)
                user.save()
                logger.info('Login successful for user "%s"' % username)
            else:
                logger.info('Agave Authentication failed: %s' % json_result)
        return user
