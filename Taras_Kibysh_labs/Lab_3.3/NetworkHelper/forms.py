from django.forms import ModelForm
from API.models import CustomerProfile

class CustomerForm(ModelForm):
    class Meta:
        model = CustomerProfile
        fields = '__all__'