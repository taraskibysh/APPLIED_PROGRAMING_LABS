from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import APIView
from yaml import serialize

from .models import *
from .repositories import *
from .serializer import CustomerSerializer, WorkerHasCustomerSerializer, WorkerSerializer, InsuranceInfoSerializer, \
    ItemInsuranceSerializer, CustomerItemSerializer, CustomerHealthSerializer
import pandas as pd

from django.shortcuts import render
class CommonMixin:
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializer
    def get(self, request, id=None):
        if id:
                user =  self.repository.get_by_id(id)
                serializer = self.serializer_class(user)
                return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            users = self.repository.get_all()
            serializer = self.serializer_class(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





    def put(self, request, id):
        user = self.repository.get_by_id(id)
        serializer = self.serializer_class(user, data=request.data, partial=True)  # `partial=True` allows updating specific fields only
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        answear = self.repository.delete(id)
        if answear:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserView(APIView, CommonMixin):
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

        result = (
            CustomerItemInsurance.objects
            .select_related('item_insurance')
            .values('price_of_item_insurance', 'item_insurance__item_price')
        )


        df = pd.DataFrame(result)


        item_price_stats = {
            'average': df['price_of_item_insurance'].mean() if not df['price_of_item_insurance'].isnull().all() else None,
            'median': df['price_of_item_insurance'].median() if not df['price_of_item_insurance'].isnull().all() else None,
            'min': df['price_of_item_insurance'].min() if not df['price_of_item_insurance'].isnull().all() else None,
            'max': df['price_of_item_insurance'].max() if not df['price_of_item_insurance'].isnull().all() else None,
        }


        insurance_price_stats = {
            'average': df['item_insurance__item_price'].mean() if not df['item_insurance__item_price'].isnull().all() else None,
            'median': df['item_insurance__item_price'].median() if not df['item_insurance__item_price'].isnull().all() else None,
            'min': df['item_insurance__item_price'].min() if not df['item_insurance__item_price'].isnull().all() else None,
            'max': df['item_insurance__item_price'].max() if not df['item_insurance__item_price'].isnull().all() else None,
        }

        return item_price_stats, insurance_price_stats


    def get_avarage_salary(self):

        result = (
            Worker.objects
            .values('position')
            .annotate(average_salary=Avg('salary'))
        )


        df = pd.DataFrame(result)


        salary_stats = {
            'average': df['average_salary'].mean(),
            'median': df['average_salary'].median(),
            'min': df['average_salary'].min(),
            'max': df['average_salary'].max(),
        }

        return salary_stats

    def get_age_information(self):
        current_year = datetime.now().year


        result = (
            CustomerProfile.objects
            .annotate(age_years=current_year - ExtractYear(F('date_of_birth')))
            .values('age_years')
        )


        df = pd.DataFrame(result)


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


        df = pd.DataFrame(result)


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


        df = pd.DataFrame(result)


        worker_capacity_stats = {
            'average': df['count'].mean(),
            'median': df['count'].median(),
            'min': df['count'].min(),
            'max': df['count'].max(),
        }

        return worker_capacity_stats

    def capacity_of_insurance_by_year(self):

        item_insurance_data = (
            CustomerItemInsurance.objects
            .values(year=ExtractYear('creation_date'))
            .annotate(count=Count('customer_insuranceinfo_id'))
            .order_by('year')
        )


        health_insurance_data = (
            CustomerHealthInsurance.objects
            .values(year=ExtractYear('creation_date'))
            .annotate(count=Count('id'))
            .order_by('year')
        )


        item_df = pd.DataFrame(item_insurance_data)
        health_df = pd.DataFrame(health_insurance_data)

        combined_df = pd.concat([item_df, health_df]).groupby('year').sum().reset_index()


        insurance_capacity_stats = {
            'average': combined_df['count'].mean(),
            'median': combined_df['count'].median(),
            'min': combined_df['count'].min(),
            'max': combined_df['count'].max(),
        }

        return insurance_capacity_stats

def show_statistics(request):
    repository = DashboardDataView()


    item_price_stats, insurance_price_stats = repository.get_basic_statistics_for_item_and_price_of_insurance()
    salary_stats = repository.get_avarage_salary()
    age_stats = repository.get_age_information()
    status_stats = repository.get_status_statistics()
    worker_capacity_stats = repository.served_people_capacity_by_worker()
    insurance_capacity_stats = repository.capacity_of_insurance_by_year()


    context = {
        'item_price_stats': item_price_stats,
        'insurance_price_stats': insurance_price_stats,
        'salary_stats': salary_stats,
        'age_stats': age_stats,
        'status_stats': status_stats,
        'worker_capacity_stats': worker_capacity_stats,
        'insurance_capacity_stats': insurance_capacity_stats,
        }


    return render(request, 'stat.html', context)