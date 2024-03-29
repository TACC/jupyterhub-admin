"""Management command."""

from django.core.management.base import BaseCommand
import logging
from jupyterhub_admin.apps.tapisauth.utils import remove_admin_user


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Command class."""

    help = (
        'Add a user to the JupyterHub Admin List'
    )


    def add_arguments(self, parser):
        parser.add_argument('username', type=str)


    def handle(self, *args, **options):
        """Handle command."""
        username = options['username']
        if not username:
            raise Exception("username required")
        logger.info("Removing admin user %s" % username)
        remove_admin_user(username)
        logger.info("Admin user %s removed" % username)
