from statistics import mode
from tabnanny import verbose
from django.db import models
from django.db import connections
# Create your models here.
class Users(models.Model):
    first_name = models.CharField(max_length=50,default='', null=False)
    last_name = models.CharField(max_length=20,default='', null=False)
    sex = models.CharField(max_length=6,default='', null=False)
    email = models.CharField(max_length=50,default='', null=False)
    aadhar=models.CharField(max_length=15,primary_key=True,default='', null=False)
    password=models.CharField(max_length=15,default='', null=False)
    
    class Meta:
        verbose_name_plural="Users"


class searchByPinorDistrinct(models.Model):
    District_name=models.CharField(max_length=6,default='',null=False)
    pin_code=models.CharField(max_length=6,default='',null=False)
    hospital_name=models.CharField(max_length=60,default='',null=False)

    class Meta:
        verbose_name_plural="searchByPin"

class appointmentDetails(models.Model):
    email = models.CharField(max_length=50,default='', null=False)
    hospital_name=models.CharField(max_length=60,default='',null=False)
    Date=models.DateField(default='',null=False)
    Time=models.CharField( max_length=20,default='',null=False)
