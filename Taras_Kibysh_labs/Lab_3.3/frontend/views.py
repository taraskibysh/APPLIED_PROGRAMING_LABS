from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import requests

# Create your views here.

base_url = "http://127.0.0.1:8000/"

# def user_list_view(request):
#     url = f"{base_url}user/"  # Вкажіть правильний URL для API
#     response = requests.get(url)
#
#     # Перевірка статусу відповіді
#     if response.status_code == 200:
#         users = response.json()  # Отримати дані користувачів
#     else:
#         users = []  # Якщо щось пішло не так, відправимо порожній список
#
#     return render(request, 'frontend/list.html', {'users': users})  #


def user_list_view(request):
    url = f"{base_url}user/"
    response = requests.get(url, cookies=request.COOKIES)  # Використовуємо кукі для аутентифікації

    if response.status_code == 200:
        users = response.json()
    else:
        users = []
        print(f"Помилка API: Статус {response.status_code}")  # Діагностика статусу відповіді

    return render(request, 'frontend/list.html', {'users': users})


def get_user(request, id):
    url = f"{base_url}user/{id}/"
    response = requests.get(url, cookies=request.COOKIES)

    if response.status_code == 200:
        user = response.json()
    else:
        user = None
        print(f"Помилка API: Статус {response.status_code}")

    return render(request, 'frontend/one_user.html', {'user': user})



