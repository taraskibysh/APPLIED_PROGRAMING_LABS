from django.shortcuts import render
from django.http import HttpResponse


def say_hello(request):
    return render(request,'hello.html')
    x = 1
    y = 2

# Create your views here.
