from operator import truediv

from django.http import QueryDict
from rest_framework.response import Response
from company.models import *
from .serializer import CustomerSerializer, WorkerHasCustomerSerializer, WorkerSerializer, InsuranceInfoSerializer
from rest_framework import generics, status



class UserRepository:

    model = None
    def __init__(self, type):
        self.model = type

    # def get(self, user_id):
    #     try:
    #         return self.obj.objects.get(id=user_id)
    #     except self.obj.DoesNotExist:
    #         return None

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

    # def get_all(self):
    #     return self.obj.objects.all()

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

    # def update(self,user_id, data):
    #
    #     user = self.obj.objects.get(id=user_id)
    #
    #     # Оновлюємо поля об'єкта за даними зі словника `data`
    #     for attr, value in data.items():
    #         setattr(user, attr, value)
    #
    #     # Зберігаємо зміни в базі даних
    #     user.save()
    #     return user


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

    # @staticmethod
    # def get_customer_by_id(self, user_id):
    #     return self.obj.objects.get(id=user_id)
    #
    # @staticmethod
    # def get_all_users():
    #     return obj.objects.all()
    #
    # @staticmethod
    # def create_user(self, data):
    #     return CustomerProfile.objects.create(**data)
    #
    # @staticmethod
    # def delete_user_by_id(self, user_id):
    #     user = CustomerProfile.objects.get(id=user_id)
    #     user.delete()
    #
    # @staticmethod
    # def update_user_by_id(self, user_id, data):
    #
    #     user = CustomerProfile.objects.get(id=user_id)
    #
    #     # Оновлюємо поля об'єкта за даними зі словника `data`
    #     for attr, value in data.items():
    #         setattr(user, attr, value)
    #
    #     # Зберігаємо зміни в базі даних
    #     user.save()
    #     return user

    # def get_worker_by_id(self, f_id, s_id):
    #     try:
    #         user = self.model.objects.get(id=f_id, customer_id=s_id)
    #         return WorkerHasCustomerProfile.objects.get(worker__id=worker_id, customer_profile__id=customer_id)
    #     except WorkerHasCustomerProfile.DoesNotExist:
    #         return None
    #
    # def get_by_id(self, user_id, serializer_class):
    #     try:
    #         user = self.model.objects.get(id=user_id)
    #         serializer = serializer_class(user)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     except self.model.DoesNotExist:
    #         return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    #
    # @staticmethod
    # def get_all_workers():
    #     return WorkerHasCustomerProfile.objects.all()
    #
    # @staticmethod
    # def delete_worker_by_id(worker_id, customer_id):
    #     item = WorkerHasCustomerProfile.objects.get(worker=worker_id, customer_profile=customer_id)
    #     item.delete()
    #
    # @staticmethod
    # def create_worker(self, data):
    #     return WorkerHasCustomerProfile(**data)