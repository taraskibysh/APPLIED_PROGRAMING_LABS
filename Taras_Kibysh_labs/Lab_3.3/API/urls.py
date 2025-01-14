from django.urls import path
from plotly.data import experiment

from .views import *
from .Diagram import *
from .Diagram2 import *
from .experiment import *

urlpatterns = [
    path('user/', UserView.as_view(), name='customer'),  # Handles POST for creating and GET for fetching all users
    path('user/<int:id>/', UserView.as_view(), name='customer_detail'),  # Handles GET, PUT, DELETE for specific user
    path('worker/', WorkerView.as_view(), name='worker'),
    path('worker/<int:worker_id>/', WorkerView.as_view(), name='worker_details'),
    path('insuranceinfo/', InsuranceInfoView.as_view(), name='insurance_info'),
    path('insuranceinfo/<int:id>/', InsuranceInfoView.as_view(), name='insurance_info_details'),
    path('item/', ItemInsuranceView.as_view(), name='insurance_info'),
    path('item/<int:id>/', ItemInsuranceView.as_view(), name='insurance_info_details'),
    path('health/', CustomerHealthView.as_view(), name='customer_health'),
    path('health/<int:id>/', CustomerHealthView.as_view(), name='customer_health_details'),
    path('whc/', WorkerHasCustomerProfileView.as_view(), name='worker_customer_profile_list'),
    path('whc/<int:f_id>,<int:s_id>/', WorkerHasCustomerProfileView.as_view(),name='worker_customer_profile_detail'),
    path('cii/', CustomerItemInsuranceView.as_view(), name='CustomerItemInsurance'),
    path('cii/<int:f_id>,<int:s_id>/', CustomerItemInsuranceView.as_view(),name='CustomerItemInsurance_details'),
    path('dashdata/', DashboardDataView.as_view(), name='dash_data'),
    path('dashboard/', combined_charts, name='insurance_dashboard'),
    path('dashboard2/', combined_charts_bokeh, name='insurance_dashboard'),
    path('stat/', show_statistics, name='dash_data'),
    path('experiment/', performance_chart, name='performance_chart' ),
    # path('salary/',average_salary_chart, name='average_salary_chart'),
]

# path('whc/', get_worker_has_customer_all, name='worker_customer_all'),
# path('whc/<int:worker_id>/', worker_details, name = 'worker_details')