from django.shortcuts import render
from django.template import loader
import os
from django.core.files.storage import default_storage
import glob
from jupyterhub_admin.apps.logdata.models import FileLog, LoginLog
from django.conf import settings
from django.contrib.auth.decorators import login_required
import logging
from itertools import chain

logger = logging.getLogger(__name__)

# Create your views here.
from django.http import HttpResponse


@login_required
def index(request):
    if request.method == 'GET':
        template = loader.get_template("logdata/index.html")

        context = {
            'error': False,
        }

        return HttpResponse(template.render(context, request))

    elif request.method == 'POST':
        template = loader.get_template("logdata/index.html")

        context = {
            'error': False,
        }
        try:
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            #tenant = settings.TENANT
            tenant = 'designsafe'
            query = ''
            if 'file_logs' in request.POST:
                context['file_logs'] = True 
                query = FileLog.objects.filter(tenant=tenant, date__range=(start_date, end_date)).order_by('date')
            elif 'login_logs' in request.POST:
                query = LoginLog.objects.filter(tenant=tenant, date__range=(start_date, end_date)).order_by('date')
            context['query'] = query
            context['queried'] = True
            if 'jhub_stats' in request.POST:
                context['jhub_stats'] = True
                context['queried'] = False
                accessed_files = FileLog.objects.filter(tenant=tenant, date__range=(start_date, end_date))
                created_files = accessed_files.filter(action='created')
                opened_files = accessed_files.filter(action='opened')
                num_created_files = created_files.count()
                num_opened_files = opened_files.count()
                login_users = LoginLog.objects.filter(tenant=tenant, date__range=(start_date, end_date))
                unique_login_count = login_users.values('user').distinct().count()
                total_login_count = login_users.count()
                try:
                    combined = list(chain(accessed_files, login_users))
                    users = []
                    for log in combined:
                        users.append(log.user)
                    unique_users = set(users)
                    unique_user_count = len(unique_users)
                except Exception as e:
                    context['error'] = True
                    context['message'] = e
                    unique_user_count = 'Error getting unique user count'
                context['num_created_files'] = num_created_files
                context['num_opened_files'] = num_opened_files
                context['unique_login_count'] = unique_login_count
                context['total_login_count'] = total_login_count
                context['unique_user_count'] = unique_user_count
                context['queried'] = False
        except Exception as e:
            context['error'] = True
            context['message'] = e

        return HttpResponse(template.render(context, request))
