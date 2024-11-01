from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import requests

# Create your views here.

base_url = "http://127.0.0.1:8000/"


def user_list_view(request):
    url = f"{base_url}user/"
    response = requests.get(url)
    users = response.json()
    return render(request, 'frontend/list.html', {users})



def User(request):
    return render(request, 'frontend/list.html')



