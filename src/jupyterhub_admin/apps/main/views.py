from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    template = loader.get_template("main/index.html")
    context = {
        'name': f"{settings.TENANT}.{settings.INSTANCE}",
        'server': settings.JUPYTERHUB_SERVER
    }
    return HttpResponse(template.render(context, request))