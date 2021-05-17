from django.http import HttpResponse
from django.template import loader
from django.conf import settings


def index(request):
    template = loader.get_template("main/index.html")
    context = {
        'name': settings.JUPYTERHUB_NAME,
        'server': settings.JUPYTERHUB_SERVER
    }
    return HttpResponse(template.render(context, request))