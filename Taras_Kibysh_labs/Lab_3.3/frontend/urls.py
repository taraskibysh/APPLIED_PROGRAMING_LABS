from django.urls import path

import frontend
from .views import *

urlpatterns = [
    path('', user_list_view, name='user_list_view'),
    path('<int:id>/', get_user, name="get_user"),
    path('delete/<int:id>/', delete_user, name="delete_user")
]

# path('whc/', get_worker_has_customer_all, name='worker_customer_all'),
# path('whc/<int:worker_id>/', worker_details, name = 'worker_details')