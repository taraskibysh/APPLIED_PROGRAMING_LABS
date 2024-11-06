from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse
from django.views import View
from requests.auth import HTTPBasicAuth


class Artist(View):



    def get(self, request, id = None):
        if id == None:
            response = requests.get('http://127.0.0.1:7000/artists/', auth=HTTPBasicAuth('Haker', '123456'))
            artists = response.json()

            return render(request, 'NetworkHelper/Get_all.html', {'artists': artists})

        else:
            response = requests.get(f'http://127.0.0.1:7000/artists/{id}', auth=HTTPBasicAuth('Haker', '123456'))
            artists = response.json()

            return render(request, 'NetworkHelper/get_one.html', {'artist': artists})



    def post(self, request, id = None):

        csrf_token = request.COOKIES.get('csrftoken')  # Отримуємо CSRF-токен з cookies

        headers = {
            'X-CSRFToken': csrf_token  # Додаємо CSRF-токен до заголовків
        }

        if id is None:
            artist_name = request.POST.get('artist_name')
            year = request.POST.get('year_of_creation')
            country = request.POST.get('country')

            data = {
                'artist_name': artist_name,
                'year_of_creation': year,
                'country': country,
            }



            response = requests.post('http://127.0.0.1:7000/artists/',
                                     data=data, headers=headers,
                                     auth=HTTPBasicAuth('Haker', '123456'))

            if response.status_code == 201:
                return redirect('artist_list_view')
            else:
                return HttpResponse(status=response.status_code)
        else:
            response = requests.delete(f'http://127.0.0.1:7000/artists/{id}/', auth=HTTPBasicAuth('Haker', '123456'))
            if response.status_code == 204:
                return redirect('artist_list_view')
            else:
                return HttpResponse(status=response.status_code)


    def put(self, request, id):
        artist_name = request.POST.get('artist_name')
        year = request.POST.get('year_of_creation')
        country = request.POST.get('country')

        csrf_token = request.COOKIES.get('csrftoken')

        headers = {
            'X-CSRFToken': csrf_token
        }

        data = {
            'artist_name': artist_name,
            'year_of_creation': year,
            'country': country,
        }



        response = requests.put(f'http://127.0.0.1:7000/artists/{id}/',headers=headers, data=data,
                                auth=HTTPBasicAuth('Haker', '123456'))



class Genre(View):

    def get(self, request, id=None):
        if id is None:
            # Get all genres
            response = requests.get('http://127.0.0.1:7000/genres/', auth=HTTPBasicAuth('Haker', '123456'))
            genres = response.json()

        else:
            # Get one genre by ID
            response = requests.get(f'http://127.0.0.1:7000/genres/{id}', auth=HTTPBasicAuth('Haker', '123456'))
            genre = response.json()


    def post(self, request, id=None):
        csrf_token = request.COOKIES.get('csrftoken')

        headers = {
            'X-CSRFToken': csrf_token
        }

        if id is None:
            # Create new genre
            genre_name = request.POST.get('genre_name')
            parent_genre_id = request.POST.get('parent_genre')

            data = {
                'genre_name': genre_name,
                'parent_genre': parent_genre_id,
            }

            response = requests.post('http://127.0.0.1:7000/genres/',
                                     data=data, headers=headers,
                                     auth=HTTPBasicAuth('Haker', '123456'))

            if response.status_code == 201:
                return redirect('genre_list_view')
            else:
                return HttpResponse(status=response.status_code)

        else:
            # Delete genre by ID
            response = requests.delete(f'http://127.0.0.1:7000/genres/{id}/', auth=HTTPBasicAuth('Haker', '123456'))
            if response.status_code == 204:
                return redirect('genre_list_view')
            else:
                return HttpResponse(status=response.status_code)

    def put(self, request, id):
        genre_name = request.POST.get('genre_name')
        parent_genre_id = request.POST.get('parent_genre')

        csrf_token = request.COOKIES.get('csrftoken')

        headers = {
            'X-CSRFToken': csrf_token
        }

        data = {
            'genre_name': genre_name,
            'parent_genre': parent_genre_id,
        }

        response = requests.put(f'http://127.0.0.1:7000/genres/{id}/', headers=headers, data=data,
                                auth=HTTPBasicAuth('Haker', '123456'))

        if response.status_code == 200:
            return redirect('genre_list_view')
        else:
            return HttpResponse(status=response.status_code)