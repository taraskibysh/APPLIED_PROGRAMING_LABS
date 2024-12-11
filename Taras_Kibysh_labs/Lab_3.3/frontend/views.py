from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
import requests
from django.shortcuts import render
from API.repositories import AggregatetedRepository


from .forms import CustomerForm

# Create your views here.

base_url = "http://127.0.0.1:8000/"


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
    response = requests.get(url, cookies=request.COOKIES)  # Отримуємо дані користувача

    if response.status_code == 200:
        user_data = response.json()  # Декодуємо дані з JSON
        form = CustomerForm(initial=user_data)  # Ініціалізуємо форму з даними користувача
    else:
        form = CustomerForm()  # Якщо не вдалося отримати дані, просто створюємо нову форму
        print(f"Помилка API: Статус {response.status_code}")

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            cleaned_data['gender'] = cleaned_data['gender'].id
            csrf_token = request.COOKIES.get('csrftoken')
            headers = {
                'X-CSRFToken': csrf_token  # Додаємо CSRF-токен до заголовків
            }

            put_response = requests.put(url, data=cleaned_data, cookies=request.COOKIES, headers=headers)

            print(f" status :{put_response.status_code}")
            if put_response.status_code == 200:  # Якщо успішно оновлено
                return redirect('get_user', id)
            else:
                form.add_error(None, "Помилка при редагуванні користувача через API")
        else:
            form.add_error(None, "Дані форми некоректні. Будь ласка, перевірте введені дані.")

    return render(request, 'frontend/change_form.html', {'form': form, 'user': user_data})



# views.py
  # Імпортуємо репозиторій для отримання даних

def dashboard(request):
    # Створюємо екземпляр репозиторія
    repo = AggregatetedRepository()

    # Отримуємо дані для дашборду
    average_salary = repo.get_avarage_salary()
    age_information = repo.get_age_information()
    status_statistics = repo.get_status_statistics()
    served_capacity = repo.served_people_capacity_by_worker()

    # Підготовка контексту для шаблону
    context = {
        'average_salary': average_salary,
        'age_information': age_information,
        'status_statistics': status_statistics,
        'served_capacity': served_capacity,
    }

    # Повертаємо рендеринг шаблону з контекстом
    return render(request, 'dashboard.html', context)
