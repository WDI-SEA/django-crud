from django.shortcuts import render
from django.http import HttpResponse

# views go here
def index(request):
  return HttpResponse('<h1>Welcome to our campus! /ᐠ｡‸｡ᐟ\ﾉ</h1>')
