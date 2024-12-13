from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import APIView
from company.models import *
from .repositories import *
from .serializer import CustomerSerializer, WorkerHasCustomerSerializer, WorkerSerializer, InsuranceInfoSerializer, \
    ItemInsuranceSerializer, CustomerItemSerializer, CustomerHealthSerializer
import pandas as pd

from django.shortcuts import render
class CommonMixin:
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request, id=None):
        if id:
            return self.repository.get_by_id(id, self.serializer_class)
        return self.repository.get_all(self.serializer_class)

    def post(self, request):
        return self.repository.create(self.serializer_class, request.data)

    def put(self, request, id):
        return self.repository.update(request.data, id, self.serializer_class)

    def delete(self, request, id):
        return self.repository.delete(id)


class UserView(APIView, CommonMixin):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializer
    repository = UserRepository(CustomerProfile)


class WorkerView(APIView, CommonMixin):
    serializer_class = WorkerSerializer
    repository = UserRepository(Worker)


class InsuranceInfoView(APIView, CommonMixin):
    serializer_class = InsuranceInfoSerializer
    repository = UserRepository(CustomerInsuranceInfo)


class ItemInsuranceView(APIView, CommonMixin):
    serializer_class = ItemInsuranceSerializer
    repository = UserRepository(ItemInsurance)

class CustomerHealthView(APIView, CommonMixin):
    serializer_class = CustomerHealthSerializer
    repository = UserRepository(CustomerHealthInsurance)




# WorkerHasCustomerProfile views

class CommonDoubleMixin:
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, f_id=None, s_id=None):
        if f_id and s_id:
            instance = self.repository.get_by_id(f_id, s_id)
            if instance is None:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            queryset = self.get_queryset()  # Use the queryset attribute
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, f_id, s_id):
        instance = self.repository.get_by_id(f_id, s_id)
        if instance is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, f_id, s_id):
        if self.repository.delete(f_id, s_id):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)



class WorkerHasCustomerProfileView(generics.GenericAPIView, CommonDoubleMixin):
    serializer_class = WorkerHasCustomerSerializer
    repository = WorkerHasCustomerRepository()

    def get_queryset(self):
        return self.repository.get_all()


class CustomerItemInsuranceView(generics.GenericAPIView, CommonDoubleMixin):
    serializer_class = CustomerItemSerializer
    repository = CustomerItemInsuranceRepository()

    def get_queryset(self):
        return self.repository.get_all()


    def put(self, request, f_id, s_id):
        instance = self.repository.get_by_id(f_id, s_id)
        if instance is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        answear = self.repository.delete(f_id, s_id)
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DashboardDataView(APIView):
    def get_basic_statistics_for_item_and_price_of_insurance(self):
        # Query to get the required data
        result = (
            CustomerItemInsurance.objects
            .select_related('item_insurance')
            .values('price_of_item_insurance', 'item_insurance__item_price')
        )

        # Convert to pandas DataFrame
        df = pd.DataFrame(result)

        # Calculate statistics for item prices
        item_price_stats = {
            'average': df['price_of_item_insurance'].mean() if not df['price_of_item_insurance'].isnull().all() else None,
            'median': df['price_of_item_insurance'].median() if not df['price_of_item_insurance'].isnull().all() else None,
            'min': df['price_of_item_insurance'].min() if not df['price_of_item_insurance'].isnull().all() else None,
            'max': df['price_of_item_insurance'].max() if not df['price_of_item_insurance'].isnull().all() else None,
        }

        # Calculate statistics for insurance prices
        insurance_price_stats = {
            'average': df['item_insurance__item_price'].mean() if not df['item_insurance__item_price'].isnull().all() else None,
            'median': df['item_insurance__item_price'].median() if not df['item_insurance__item_price'].isnull().all() else None,
            'min': df['item_insurance__item_price'].min() if not df['item_insurance__item_price'].isnull().all() else None,
            'max': df['item_insurance__item_price'].max() if not df['item_insurance__item_price'].isnull().all() else None,
        }

        return item_price_stats, insurance_price_stats

    def generate_statistics_html(self, item_price_stats, insurance_price_stats):
        # Load the template for displaying the statistics
        html_output = render_to_string('statistics_template.html', {
            'item_price_stats': item_price_stats,
            'insurance_price_stats': insurance_price_stats,
        })

        # Return the rendered HTML as an HttpResponse
        return HttpResponse(html_output)

    def get_avarage_salary(self):
        # Get average salary per position using pandas
        result = (
            Worker.objects
            .values('position')
            .annotate(average_salary=Avg('salary'))
        )

        # Convert to pandas DataFrame
        df = pd.DataFrame(result)

        # Calculate statistics for salary
        salary_stats = {
            'average': df['average_salary'].mean(),
            'median': df['average_salary'].median(),
            'min': df['average_salary'].min(),
            'max': df['average_salary'].max(),
        }

        return salary_stats

    def get_age_information(self):
        current_year = datetime.now().year  # Current year

        # Retrieve age data and group it
        result = (
            CustomerProfile.objects
            .annotate(age_years=current_year - ExtractYear(F('date_of_birth')))
            .values('age_years')
        )

        # Convert to pandas DataFrame
        df = pd.DataFrame(result)

        # Calculate statistics for age
        age_stats = {
            'average': df['age_years'].mean() if not df['age_years'].isnull().all() else None,
            'median': df['age_years'].median() if not df['age_years'].isnull().all() else None,
            'min': df['age_years'].min() if not df['age_years'].isnull().all() else None,
            'max': df['age_years'].max() if not df['age_years'].isnull().all() else None,
        }

        return age_stats

    def get_status_statistics(self):
        result = (
            CustomerInsuranceInfo.objects
            .values('status__status')
            .annotate(count=Count('status'))
            .order_by('-count')
        )

        # Convert to pandas DataFrame
        df = pd.DataFrame(result)

        # Calculate statistics for the count of statuses
        status_stats = {
            'average': df['count'].mean(),
            'median': df['count'].median(),
            'min': df['count'].min(),
            'max': df['count'].max(),
        }

        return status_stats

    def served_people_capacity_by_worker(self):
        result = (
            WorkerHasCustomerProfile.objects
            .values("worker")
            .annotate(count=Count("customer_profile"))
            .order_by('-count')
        )

        # Convert to pandas DataFrame
        df = pd.DataFrame(result)

        # Calculate statistics for worker capacity
        worker_capacity_stats = {
            'average': df['count'].mean(),
            'median': df['count'].median(),
            'min': df['count'].min(),
            'max': df['count'].max(),
        }

        return worker_capacity_stats

    def capacity_of_insurance_by_year(self):
        # First query for customer_item_insurance
        item_insurance_data = (
            CustomerItemInsurance.objects
            .values(year=ExtractYear('creation_date'))
            .annotate(count=Count('customer_insuranceinfo_id'))
            .order_by('year')
        )

        # Second query for customer_health_insurance
        health_insurance_data = (
            CustomerHealthInsurance.objects
            .values(year=ExtractYear('creation_date'))
            .annotate(count=Count('id'))
            .order_by('year')
        )

        # Combine results
        item_df = pd.DataFrame(item_insurance_data)
        health_df = pd.DataFrame(health_insurance_data)

        combined_df = pd.concat([item_df, health_df]).groupby('year').sum().reset_index()

        # Calculate statistics for insurance capacity by year
        insurance_capacity_stats = {
            'average': combined_df['count'].mean(),
            'median': combined_df['count'].median(),
            'min': combined_df['count'].min(),
            'max': combined_df['count'].max(),
        }

        return insurance_capacity_stats

def show_statistics(request):
    repository = DashboardDataView()

    # Fetch all statistics data
    item_price_stats, insurance_price_stats = repository.get_basic_statistics_for_item_and_price_of_insurance()
    salary_stats = repository.get_avarage_salary()
    age_stats = repository.get_age_information()
    status_stats = repository.get_status_statistics()
    worker_capacity_stats = repository.served_people_capacity_by_worker()
    insurance_capacity_stats = repository.capacity_of_insurance_by_year()

        # Prepare all the data to be passed to the template
    context = {
        'item_price_stats': item_price_stats,
        'insurance_price_stats': insurance_price_stats,
        'salary_stats': salary_stats,
        'age_stats': age_stats,
        'status_stats': status_stats,
        'worker_capacity_stats': worker_capacity_stats,
        'insurance_capacity_stats': insurance_capacity_stats,
        }

    # Render the HTML response with the context
    return render(request, 'stat.html', context)