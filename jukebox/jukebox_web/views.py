# -*- coding: UTF-8 -*-

from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout as auth_logout
from django.template import RequestContext
from django.utils import simplejson
from django.contrib.messages.api import get_messages
from django.conf import settings
from jukebox_core.models import Song, Artist, Album, Genre, \
                                Queue, Favourite, History

def index(request):
    if request.user.is_authenticated():
        request.session.set_expiry(settings.SESSION_TTL)

        genres = Genre.objects.all()
        years = Song.objects.values("Year").distinct()
        years = years.exclude(Year=None).exclude(Year=0).order_by("Year")

        context = {
            "username": request.user.get_full_name(),
            "genres": genres,
            "years": years
        }
        context.update(csrf(request))
        return render_to_response('index.html', context)
    else:
        return HttpResponseRedirect('login')

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('index')
    else:
        return render_to_response(
            'login.html',
            {
                "backends": settings.SOCIAL_AUTH_ENABLED_BACKENDS,
            },
            RequestContext(request)
        )

def login_error(request):
    messages = get_messages(request)
    return render_to_response(
        'login.html',
        {"error": messages},
        RequestContext(request)
    )

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

def ping(request):
    request.session.modified = True
    return HttpResponse(
        simplejson.dumps({"ping": True}),
        mimetype="application/json"
    )