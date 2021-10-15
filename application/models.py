from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name)
    
class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/PatientProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    doctor_id  = models.PositiveIntegerField(blank=True, null=True)
    anamnesi_personale = models.FileField(upload_to='files/',null=True, blank=True)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{}".format(self.user.first_name)

class dataset(models.Model):
    codice_patologia = models.CharField(max_length=255)
    patologia = models.CharField(max_length=255)
    codice_sintomo = models.CharField(max_length=255)
    sintomo = models.CharField(max_length=255)
    sintomo_principale = models.CharField(max_length=255)
    def _str_(self):
        return self.codice_patologia

