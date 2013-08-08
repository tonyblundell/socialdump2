from django.shortcuts import render_to_response
from main.models import Feed

def index(request):
    template = 'main/index.html'
    context = {
        'feeds': Feed.objects.all()
    }
    return render_to_response(template, context)
