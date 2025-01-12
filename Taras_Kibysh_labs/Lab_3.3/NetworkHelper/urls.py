from django.urls import path
from .NetworkHelper import Artist

import NetworkHelper
from .views import *

urlpatterns = [
    path('', user_list_view, name='user_list_view'),
    path('<int:id>/', get_user, name="get_user"),
    path('delete/<int:id>/', delete_user, name="delete_user"),
    path('create/', create_user, name="create_user"),
    path('change/<int:id>/', change_user, name="change_user"),
    path('artist/', Artist.as_view(), name='artist_list_view'),
    path('artist/<int:id>/', Artist.as_view(), name='artist_view'),
    path('artist/delete/<int:id>/', Artist.as_view(), name='delete_artist'),
    path('artist/create/', Artist.as_view(), name='create_artist')
]


# path('whc/', get_worker_has_customer_all, name='worker_customer_all'),
# path('whc/<int:worker_id>/', worker_details, name = 'worker_details')