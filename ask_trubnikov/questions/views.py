from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render


def hello_world(request):
    return HttpResponse("<i>Hello, Django!</i>")

def template(request):
    return render(request, "for_views.html")

def reqGetPost(request):
    if (request.method == 'GET'):
        get = request.GET.urlencode()
        get = get.decode().replace('&', '<br>')
        return HttpResponse("<h3>Get request:</h3>" + get)
    if (request.method == 'POST'):
        post = request.POST
        return HttpResponse("<h3>Post request:</h3>" + post)
    return HttpResponse("<h3>Another request<h3>")
