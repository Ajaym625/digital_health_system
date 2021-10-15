from django import forms
from django.contrib.auth.models import User
from . import models

#Doctor Registration
class DoctorRegisterForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class DoctorForm(forms.ModelForm):
    class Meta:
        model=models.Doctor
        fields=['address','mobile','profile_pic']



#patient Registration
class PatientRegisterForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class PatientForm(forms.ModelForm):
    # doctor_id=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(), to_field_name="user_id")
    class Meta:
        model=models.Patient
        fields=['address','mobile','profile_pic','doctor_id','anamnesi_personale']

class dataset(forms.ModelForm):
    class Meta:
        model=models.dataset
        fields=['codice_patologia', 'patologia', 'codice_sintomo', 'sintomo', 'sintomo_principale']
