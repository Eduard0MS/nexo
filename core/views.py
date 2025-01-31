from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def hello(request, user):
    return HttpResponse('<h1>Hello {}</h1>'.format(user))