from abc import ABC, abstractmethod
from company.models import CustomerProfile

class CustomerRepositoryInterface(ABC):

    @abstractmethod
    def get_all_customers(self):
        pass

    @abstractmethod
    def get_customer_by_id(self, id):
        pass

    @abstractmethod
    def get_customer_by_name(self, name):
        pass

    @abstractmethod
    def create_customer(self):
        pass

    @abstractmethod
    def update_customer(self, id):
        pass

    @abstractmethod
    def delete_customer(self, id):
        pass