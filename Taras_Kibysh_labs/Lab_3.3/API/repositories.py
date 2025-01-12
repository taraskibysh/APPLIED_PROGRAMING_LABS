from operator import truediv
from django.http import QueryDict
from rest_framework.response import Response
from .models import *
from .serializer import CustomerSerializer, WorkerHasCustomerSerializer, WorkerSerializer, InsuranceInfoSerializer
from rest_framework import generics, status
from django.db.models import  ExpressionWrapper, IntegerField, F, Value, Count, Case, When, CharField, Q, Avg, DecimalField
from django.db.models.functions import Now, ExtractYear, Concat
from datetime import datetime
from collections import defaultdict
from rest_framework.exceptions import NotFound





class UserRepository:

    model = None
    def __init__(self, type):
        self.model = type



    def get_by_id(self, user_id):
        try:
            user = self.model.objects.get(id=user_id)
            return user
        except self.model.DoesNotExist:
            raise NotFound(f"User with id {user_id} does not exist")

    def get_all(self):
        users = self.model.objects.all()
        return users

    def delete(self,user_id):
        user = self.model.objects.get(id=user_id)
        if user:
            user.delete()
            return True
        else:
            return False




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
                    Avg("salary"),
                    output_field=DecimalField()
                )
            )
            .order_by("average")
        )
        return result


    def get_age_information(self):
        current_year = datetime.now().year

        result = (
            CustomerProfile.objects.annotate(
                age_years=current_year - ExtractYear(F('date_of_birth'))
            )
            .annotate(
                age_group=Case(
                    When(age_years__lt=20, then=Value('0-20')),
                    When(age_years__gte=20, age_years__lt=40, then=Value('20-40')),
                    When(age_years__gte=40, age_years__lt=60, then=Value('40-60')),
                    default=Value('Other'),
                    output_field=CharField(),
                )
            )
            .values('age_group')
            .annotate(
                male_count=Count('id', filter=Q(gender__gender_name='male')),
                female_count=Count('id', filter=Q(gender__gender_name='female'))
            )
            .order_by('age_group')
        )
        return result


    def get_status_statistics(self):
        result = (
            CustomerInsuranceInfo.objects
            .values('status__status')
            .annotate(count=Count('status'))
            .order_by('-count')
        )

        return result

    def served_people_capacity_by_worker(self):
        result = (
            WorkerHasCustomerProfile.objects
            .values("worker")
            .annotate(
                worker_name=Concat(F('worker__name'), Value(' '), F('worker__surname'))
            )
            .annotate(count=Count("customer_profile"))
            .order_by('-count')
        )
        return result

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


        combined_data = defaultdict(int)


        for record in item_insurance_data:
            combined_data[record['year']] += record['count']


        for record in health_insurance_data:
            combined_data[record['year']] += record['count']


        final_result = [{'year': year, 'total_count': count} for year, count in combined_data.items()]

        # Сортування за роком
        final_result.sort(key=lambda x: x['year'])


        return final_result


    def get_price_of_item_and_price_of_insurance(self):
        result = (
            CustomerItemInsurance.objects
            .select_related('item_insurance')
            .values( 'price_of_item_insurance', 'item_insurance__item_price')
        )
        return result



