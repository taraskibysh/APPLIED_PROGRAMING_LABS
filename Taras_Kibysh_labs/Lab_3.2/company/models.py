from django.db import models



class CustomerProfile(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=45)  # Field name made lowercase.
    surname = models.CharField(max_length=45)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    gender = models.ForeignKey('Gender', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'customer_profile'
    def __str__(self):
        return self.name + " " + self.surname




class Gender(models.Model):
    gender_name = models.CharField(unique=True, max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'gender'
    def __str__(self):
        return self.gender_name


class Worker(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    position = models.CharField(max_length=45)
    salary = models.DecimalField(max_digits = 10, decimal_places= 2, blank=True, null=True)
    Customers = models.ManyToManyField(CustomerProfile, through='WorkerHasCustomerProfile')


    def __str__(self):
        manage = False
        return self.name + " " + self.surname

    class Meta:
        db_table = 'worker'

class WorkerHasCustomerProfile(models.Model):
    worker = models.ForeignKey('Worker', db_column='fk_worker_id', on_delete=models.DO_NOTHING, primary_key=True)
    customer_profile = models.ForeignKey('CustomerProfile', db_column='fk_customer_id', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'worker_has_customer_profile'

    def __str__(self):
        return f"{self.worker} - {self.customer_profile}"


class Status(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    status = models.CharField(db_column='status', max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'status'

    def __str__(self):
        return f"{self.status}"



class TypeOfInsurance(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    type = models.CharField(db_column='type_of_insurance', max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'type_of_insurance'

    def __str__(self):
        return f"{self.type}"





class CustomerInsuranceInfo(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    CustomerProfile = models.ForeignKey('CustomerProfile', models.DO_NOTHING, db_column='customer_profile_ID', blank=True, null=True)  # Field name made lowercase.
    type_of_insurance = models.ForeignKey('typeOfInsurance', models.DO_NOTHING, blank=True, null=True)
    status = models.ForeignKey('Status', models.DO_NOTHING, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'customer_insuranceinfo'

    def __str__(self):
        return f"{self.CustomerProfile.name} - {self.CustomerProfile.surname}"

class Checklist(models.Model):

    name_of_disease = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'checklist'
    def __str__(self):
        return f"{self.name_of_disease}"

class CustomerHealthInsurance(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    customer_insuranceinfo = models.ForeignKey('CustomerInsuranceInfo', models.DO_NOTHING, blank=True, null=False)
    checklist = models.ForeignKey('Checklist', models.DO_NOTHING, blank=True, null=True)
    name_of_the_hospital = models.CharField(max_length=45, blank=True, null=True)
    price_of_health_insurance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_health_insurance'


class ItemInsurance(models.Model):
    item_name = models.CharField(max_length=45)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'item_insurance'

    def __str__(self):
        return f"{self.item_name}"


class CustomerItemInsurance(models.Model):
    customer_insuranceinfo = models.ForeignKey('CustomerInsuranceInfo', models.DO_NOTHING, null=False, primary_key= True)  # The composite primary key (customer_insuranceinfo_id, item_insurance_id) found, that is not supported. The first column is selected.
    item_insurance = models.ForeignKey('ItemInsurance', models.DO_NOTHING)
    price_of_item_insurance = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'customer_item_insurance'
        # unique_together = (('customer_insuranceinfo', 'item_insurance'),)