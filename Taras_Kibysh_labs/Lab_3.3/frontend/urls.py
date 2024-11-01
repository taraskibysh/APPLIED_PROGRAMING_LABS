from django.urls import path

import frontend
from .views import *

urlpatterns = [
    path('', user_list_view, name='frontend'),
]

# path('whc/', get_worker_has_customer_all, name='worker_customer_all'),
# path('whc/<int:worker_id>/', worker_details, name = 'worker_details')