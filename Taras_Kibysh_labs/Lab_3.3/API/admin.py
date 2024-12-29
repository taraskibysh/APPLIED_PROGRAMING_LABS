from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomerProfile, Worker, WorkerHasCustomerProfile, CustomerInsuranceInfo, CustomerHealthInsurance, \
    Status, TypeOfInsurance, Gender, CustomerItemInsurance


class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'surname', 'date_of_birth', 'phone_number', 'get_gender_name')
    search_fields = ('id', 'name', 'surname')


    def get_gender_name(self, obj):
        return obj.gender.gender_name
    get_gender_name.short_description = 'Gender'


class WorkerHasCustomerProfileAdmin(admin.ModelAdmin):
      list_display =('worker', 'customer_profile')


class WorkerAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'surname', 'position', 'salary')
    search_display = ('id', 'name', 'surname')



class CustomerInsuranceInfoAdmin(admin.ModelAdmin):
    list_display = ('id','customer_name', 'status_def', 'type_of_insurance_def')


    def customer_name(self, obj):
        return f"{obj.CustomerProfile.name} {obj.CustomerProfile.surname}"
    customer_name.short_description = 'Customer'

    def type_of_insurance_def(self, obj):
        return obj.type_of_insurance.type

    def status_def(self, obj):
        return obj.status.status



class CustomerHealthInsuranceAdmin(admin.ModelAdmin):
    list_display = ('id', 'checklist', 'price_of_health_insurance', 'creation_date')

class CustomerItemInsuranceAdmin(admin.ModelAdmin):
    list_display = ( 'customer_insuranceinfo', 'item_insurance', 'price_of_item_insurance', 'creation_date')



admin.site.register(Status)
admin.site.register(TypeOfInsurance)
admin.site.register(Gender)

admin.site.register(CustomerItemInsurance, CustomerItemInsuranceAdmin)
admin.site.register(CustomerHealthInsurance, CustomerHealthInsuranceAdmin)
admin.site.register(CustomerProfile, CustomerProfileAdmin )
admin.site.register(Worker, WorkerAdmin)
admin.site.register(WorkerHasCustomerProfile, WorkerHasCustomerProfileAdmin)
admin.site.register(CustomerInsuranceInfo, CustomerInsuranceInfoAdmin)


# Register your models here.
