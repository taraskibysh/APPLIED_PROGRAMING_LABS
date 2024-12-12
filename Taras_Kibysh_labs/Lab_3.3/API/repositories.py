from operator import truediv
from django.http import QueryDict
from rest_framework.response import Response
from company.models import *
from .serializer import CustomerSerializer, WorkerHasCustomerSerializer, WorkerSerializer, InsuranceInfoSerializer
from rest_framework import generics, status
from django.http import QueryDict
from rest_framework.response import Response
from django.db.models import  ExpressionWrapper, IntegerField, F, Value, Count, Case, When, CharField, Q, Avg
from django.db.models.functions import Now, ExtractYear, Concat
from datetime import datetime
from django.http import QueryDict
from rest_framework.response import Response
from company.models import *
from .serializer import CustomerSerializer, WorkerHasCustomerSerializer, WorkerSerializer, InsuranceInfoSerializer
from rest_framework import generics, status
from django.db.models import  ExpressionWrapper, IntegerField, F, Value, Count, Case, When, CharField, Q, Avg, DecimalField
from django.db.models.functions import Now, ExtractYear, Concat
from datetime import datetime
from collections import defaultdict




class UserRepository:

    model = None
    def __init__(self, type):
        self.model = type



    def get_by_id(self, user_id, serializer_class):
        try:
            user = self.model.objects.get(id=user_id)
            serializer = serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except self.model.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def get_all(self, serializer_class):
        users = self.model.objects.all()
        serializer = serializer_class(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, serializer_class, data):
        # Convert QueryDict to a regular dictionary if neede

        serializer = serializer_class(data=data)  # Pass the cleaned data to serializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def update(self, data, user_id, serializer_class):
        # Ensure `data` is in dictionary form if passed as a `QueryDict`

        # Retrieve the user instance directly
        try:
            user = self.model.objects.get(id=user_id)
        except self.model.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        # Pass the user instance and updated data to the serializer
        serializer = serializer_class(user, data=data, partial=True)  # `partial=True` allows updating specific fields only
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def delete(self,user_id):
        user = self.model.objects.get(id=user_id)
        if user:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)




class CustomerItemInsuranceRepository:
    model = CustomerItemInsurance

    def get_by_id(self, f_id, s_id):
        try:
            user = self.model.objects.get(customer_insuranceinfo=f_id, item_insurance=s_id)
            return user
        except CustomerItemInsurance.DoesNotExist:
            return None


    def get_all(self):
        return self.model.objects.all()


    def delete(self,worker_id, customer_id):
        item = self.model.objects.get(customer_insuranceinfo=worker_id, item_insurance=customer_id)
        item.delete()


    def create(self, data):
        return WorkerHasCustomerProfile(**data)

class WorkerHasCustomerRepository:
    model = WorkerHasCustomerProfile

    def get_by_id(self, f_id, s_id):
        try:
            user = self.model.objects.get(worker_id=f_id, customer_profile_id=s_id)
            return user
        except WorkerHasCustomerProfile.DoesNotExist:
            return None

    def get_all(self):
        return self.model.objects.all()

    def delete(self, worker_id, customer_id):
        item = self.model.objects.get(worker=worker_id, customer_profile=customer_id)
        item.delete()

    def create(self, data):
        return WorkerHasCustomerProfile(**data)


class AggregatetedRepository:

    def get_avarage_salary(self):
        result = (
            Worker.objects
            .values("position")
            .annotate(
                average=ExpressionWrapper(
                    Avg("salary"),  # Явно вказуємо тип для 'position'
                    output_field=DecimalField()  # Вказуємо результат як DecimalField
                )
            )
            .order_by("average")
        )
        return result


    def get_age_information(self):
        current_year = datetime.now().year  # Поточний рік

        result = (
            CustomerProfile.objects.annotate(
                age_years=current_year - ExtractYear(F('date_of_birth'))  # Обчислюємо вік
            )
            .annotate(
                age_group=Case(
                    When(age_years__lt=20, then=Value('0-20')),
                    When(age_years__gte=20, age_years__lt=40, then=Value('20-40')),
                    When(age_years__gte=40, age_years__lt=60, then=Value('40-60')),
                    default=Value('Other'),
                    output_field=CharField(),  # Виправлення на CharField
                )
            )
            .values('age_group')  # Групуємо за категорією віку
            .annotate(
                male_count=Count('id', filter=Q(gender__gender_name='male')),  # Підрахунок чоловіків
                female_count=Count('id', filter=Q(gender__gender_name='female'))  # Підрахунок жінок
            )
            .order_by('age_group')  # Сортування за категорією
        )
        return result


    def get_status_statistics(self):
        result = (
            CustomerInsuranceInfo.objects
            .values('status')  # Групуємо за статусом
            .annotate(count=Count('status'))  # Підрахунок кількості за статусом
            .order_by('-count')  # Сортуємо за кількістю у порядку спадання
        )

        return result

    def served_people_capacity_by_worker(self):
        result = (
            WorkerHasCustomerProfile.objects
            .values("worker")  # Вибираємо лише "worker" (не виводимо id)
            .annotate(
                worker_name=Concat(F('worker__name'), Value(' '), F('worker__surname'))  # Створюємо ім'я + прізвище
            )
            .annotate(count=Count("customer_profile"))  # Підраховуємо кількість
            .order_by('-count')  # Сортуємо за кількістю
        )
        return result

    def capacity_of_insurance_by_year(self):
        # Перший запит для `customer_item_insurance`
        item_insurance_data = (
            CustomerItemInsurance.objects
            .values(year=ExtractYear('creation_date'))
            .annotate(count=Count('customer_insuranceinfo_id'))
            .order_by('year')
        )

        # Другий запит для `customer_health_insurance`
        health_insurance_data = (
            CustomerHealthInsurance.objects
            .values(year=ExtractYear('creation_date'))
            .annotate(count=Count('id'))
            .order_by('year')
        )

        # Об'єднання результатів
        combined_data = defaultdict(int)

        # Додавання результатів для `customer_item_insurance`
        for record in item_insurance_data:
            combined_data[record['year']] += record['count']

        # Додавання результатів для `customer_health_insurance`
        for record in health_insurance_data:
            combined_data[record['year']] += record['count']

        # Підготовка фінального результату
        final_result = [{'year': year, 'total_count': count} for year, count in combined_data.items()]

        # Сортування за роком
        final_result.sort(key=lambda x: x['year'])

        # Виведення результатів
        return final_result



