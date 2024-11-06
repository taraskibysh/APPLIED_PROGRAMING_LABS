from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import APIView
from company.models import *
from .repositories import UserRepository, WorkerHasCustomerRepository, CustomerItemInsuranceRepository
from .serializer import CustomerSerializer, WorkerHasCustomerSerializer, WorkerSerializer, InsuranceInfoSerializer, \
    ItemInsuranceSerializer, CustomerItemSerializer, CustomerHealthSerializer


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




