import os
import django
import re
from datetime import datetime
import json
import logging
from collections import defaultdict
import sys
import gzip

os.environ["DJANGO_SETTINGS_MODULE"] = "jupyterhub_admin.settings"
django.setup()

from jupyterhub_admin.apps.logdata.models import Tenant, TenantDirectory, TenantRecipient

tenant_configs = [
    {
        'name': 'designsafe',
        'proper_name': 'DesignSafe',
        'directories': ['CommunityData', 'MyData', 'MyProjects', 'NEES', 'NHERI-Published'],
        'primary_receiver': 'jfreeze@tacc.utexas.edu',
        'recipients': ['jfreeze@tacc.utexas.edu', 'jstubbs@tacc.utexas.edu', 'ajamthe@tacc.utexas.edu', 'gcurbelo@tacc.utexas.edu', 'hammock@tacc.utexas.edu']
    },
    {
        'name': 'tacc',
        'proper_name': 'TACC',
        'directories': ['team_classify', 'Hobby-Eberly-Telesco', 'HETDEX-Work', 'Hobby-Eberly-Public', 'work'],
        'primary_receiver': 'jstubbs@tacc.utexas.edu',
        'recipients': ['jstubbs@tacc.utexas.edu', 'ajamthe@tacc.utexas.edu', 'gcurbelo@tacc.utexas.edu', 'hammock@tacc.utexas.edu']
    },
]

def add_tenant_configs():
    for conf in tenant_configs:
        tenant = conf['name']
        primary_receiver = conf['primary_receiver']
        proper_name = conf['proper_name']
        entry = Tenant(
            tenant=tenant,
            primary_receiver=primary_receiver,
            proper_name=proper_name
        )
        entry.save()
        directories = conf['directories']
        recipients = conf['recipients']
        for directory in directories:
            dir = TenantDirectory(
                tenant=entry,
                directory=directory
            )
            dir.save()
        for recipient in recipients:
            rec = TenantRecipient(
                tenant=entry,
                recipient=recipient
            )
            rec.save()

add_tenant_configs()

