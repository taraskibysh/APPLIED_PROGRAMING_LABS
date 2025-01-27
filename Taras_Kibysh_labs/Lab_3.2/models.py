# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Checklist(models.Model):
    name_of_disease = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'checklist'


class CustomerHealthInsurance(models.Model):
    customer_insuranceinfo = models.ForeignKey('CustomerInsuranceinfo', models.DO_NOTHING, blank=True, null=True)
    checklist = models.ForeignKey(Checklist, models.DO_NOTHING, blank=True, null=True)
    name_of_the_hospital = models.CharField(max_length=45, blank=True, null=True)
    price_of_healt_insurance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_health_insurance'


class CustomerInsuranceinfo(models.Model):
    customer_profile = models.ForeignKey('CustomerProfile', models.DO_NOTHING, db_column='customer_profile_ID', blank=True, null=True)  # Field name made lowercase.
    type_of_insurance = models.ForeignKey('TypeOfInsurance', models.DO_NOTHING, blank=True, null=True)
    status = models.ForeignKey('Status', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_insuranceinfo'


class CustomerItemInsurance(models.Model):
    customer_insuranceinfo = models.OneToOneField(CustomerInsuranceinfo, models.DO_NOTHING, primary_key=True)  # The composite primary key (customer_insuranceinfo_id, item_insurance_id) found, that is not supported. The first column is selected.
    item_insurance = models.ForeignKey('ItemInsurance', models.DO_NOTHING)
    price_of_item_insurance = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'customer_item_insurance'
        unique_together = (('customer_insuranceinfo', 'item_insurance'),)


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


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Gender(models.Model):
    gender_name = models.CharField(unique=True, max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gender'


class ItemInsurance(models.Model):
    item_name = models.CharField(max_length=45)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'item_insurance'


class Status(models.Model):
    status = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'status'


class TypeOfInsurance(models.Model):
    type_of_insurance = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'type_of_insurance'


class Worker(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    position = models.CharField(max_length=45)
    salary = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'worker'


class WorkerHasCustomerProfile(models.Model):
    id = models.AutoField(DB_column='id',primary_key=True)
    worker = models.ForeignKey(Worker, models.DO_NOTHING, db_column='worker_ID')
    customer_profile = models.ForeignKey(CustomerProfile, models.DO_NOTHING, db_column='customer_profile_ID', null=True)  # Додано null=True

    class Meta:
        db_table = 'worker_has_customer_profile'
        unique_together = (('worker', 'customer_profile'),)

    def __str__(self):
        return f"{self.worker} - {self.customer_profile}"



# class WorkerHasCustomerProfile(models.Model):
#     worker = models.OneToOneField(Worker, models.DO_NOTHING, db_column='worker_ID', primary_key=True)  # Field name made lowercase. The composite primary key (worker_ID, customer_profile_ID) found, that is not supported. The first column is selected.
#     customer_profile = models.ForeignKey(CustomerProfile, models.DO_NOTHING, db_column='customer_profile_ID')  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'worker_has_customer_profile'
#         unique_together = (('worker', 'customer_profile'),)
