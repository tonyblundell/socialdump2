from django.conf import settings
from django.shortcuts import render_to_response
from main.models import Feed

def index(request):
    template = 'main/index.html'
    context = {
        'feeds': Feed.objects.all(),
        'title': settings.SD2_TITLE,
        'subtitle': settings.SD2_SUBTITLE,
        'mail': settings.SD2_MAIL,
    }
    return render_to_response(template, context)
