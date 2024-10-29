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


class TypeOfInsurance(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    type = models.CharField(db_column='type_of_insurance', max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'type_of_insurance'


class CustomerInsuranceInfo(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    CustomerProfile = models.ForeignKey('CustomerProfile', models.DO_NOTHING, db_column='customer_profile_ID', blank=True, null=True)  # Field name made lowercase.
    type_of_insurance = models.ForeignKey('typeOfInsurance', models.DO_NOTHING, blank=True, null=True)
    status = models.ForeignKey('Status', models.DO_NOTHING, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'customer_insuranceinfo'
