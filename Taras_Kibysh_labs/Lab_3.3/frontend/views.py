from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
import requests

from openid.extensions.draft.pape5 import Request

from .forms import CustomerForm

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



def delete_user(request, id):
    url = f"{base_url}user/{id}/"
    csrf_token = request.COOKIES.get('csrftoken')  # Отримуємо CSRF-токен з cookies

    headers = {
        'X-CSRFToken': csrf_token  # Додаємо CSRF-токен до заголовків
    }

    # Додаємо заголовки до запиту
    response = requests.delete(url, headers=headers, cookies=request.COOKIES)
    print(F"problem {response.content}")

    # Проверка, был ли запрос успешным
    if response.status_code == 204:
        # Якщо успішно, перенаправляємо на список користувачів
        return redirect('user_list_view')
    else:
        print(f"{response.content} status: + {response.status_code}")
        # Обробка помилок
        return redirect('user_list_view')  # Укажите вашу страницу ошибок или другую логику


def create_user(request):
    url = f"{base_url}user/"
    form = CustomerForm(None)

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            cleaned_data['gender'] = cleaned_data['gender'].id
            response = requests.post(url, data=cleaned_data)
            if response.status_code == 201:  # Якщо успішно створено
                return redirect('user_list_view')
            else:
                form.add_error(None, "Помилка при створенні користувача через API")
        else:
            form.add_error(None, "Дані форми некоректні. Будь ласка, перевірте введені дані.")

    context = {'form': form}
    print("hello world")
    return render(request, 'frontend/create_form.html', context)



def change_user(request, id):
    url = f"{base_url}user/{id}/"
    form = CustomerForm()

    response = requests.get(url, cookies=request.COOKIES)  # Використовуємо кукі для аутентифікації

    if response.status_code == 200:
        user = response.json()
    else:
        user = []
        print(f"Помилка API: Статус {response.status_code}")


    # if request.method == 'POST':
    #         form = CustomerForm(request.POST)
    #         if form.is_valid():
    #             cleaned_data = form.cleaned_data
    #             cleaned_data['gender'] = cleaned_data['gender'].id
    #             put_response = requests.put(url, data=cleaned_data, cookies=request.COOKIES)
    #
    #             if put_response.status_code == 200:  # If successfully updated
    #                 return redirect('get_user', id)
    #             else:
    #                 form.add_error(None, "Error updating user via API")
    #         else:
    #             form.add_error(None, "Form data is invalid. Please check your input.")

    return render(request, 'frontend/change_form.html', {'user': user})
