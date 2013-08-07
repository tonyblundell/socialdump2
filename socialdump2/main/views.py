from django.shortcuts import render_to_response

def index(request):
    template = 'main/index.html'
    context = {}
    return render_to_response(template, context)
