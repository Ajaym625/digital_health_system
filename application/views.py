from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.db.models import Q
from django.contrib import messages

TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates")'
)

# Create your views here.

def index(request):
    return render(request,'home/index.html')

def doctor_landing(request):
    return render(request,'doctor/doctor_landing.html')

def patient_landing(request):
    return render(request,'patient/patient_landing.html')

# def doctor_login(request):

#     return render(request,'doctor/doctor_login.html')

def doctor_register(request):
    userForm=forms.DoctorRegisterForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorRegisterForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST,request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor=doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
            messages.success(request, 'Doctor account created Successfully')
        return HttpResponseRedirect('/doctor/login/')
    return render(request,'doctor/doctor_register.html',context=mydict)

# def patient_login(request):
#     return render(request,'patient/patient_login.html')

def patient_register(request):
    userForm=forms.PatientRegisterForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientRegisterForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient=patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
            messages.success(request, 'Patient account created Successfully')
        return HttpResponseRedirect('/patient/login/')
    return render(request,'patient/patient_register.html',context=mydict)


#User Group
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()

#after login 
def post_login_view(request):
    if is_doctor(request.user):
        return redirect('dashboard_doctor')
        
    elif is_patient(request.user):
        return redirect('dashboard_patient')
        


##### doctor View Methods 
@login_required(login_url='doctor/login')
@user_passes_test(is_doctor)
def dashboard_doctor_view(request):
    return render(request,'doctor/dashboard_doctor.html')


@login_required(login_url='doctor/login')
@user_passes_test(is_doctor)
def patient_list(request):
    patients=models.Patient.objects.filter(doctor_id__isnull=True)
    doc_id = request.user.id
    return render(request,'doctor/patient_list.html',{'patients':patients,'doc_id':doc_id})


@login_required(login_url='doctor/login')
@user_passes_test(is_doctor)
def patient_selection(request):
    patient=models.Patient.objects.get(id=request.POST.get('patient_id'))
    if request.method=='POST':
        patient.doctor_id= request.POST.get('doc_id')
        patient.save()
        return redirect('patient_list')
    return render(request,'doctor/patient_list.html')


@login_required(login_url='doctor/login')
@user_passes_test(is_doctor)
def visualize_patient(request):
    patients=models.Patient.objects.filter(doctor_id__isnull=False, doctor_id=request.user.id)
    return render(request,'doctor/visualize_patient.html',{'patients':patients})


@login_required(login_url='doctor/login')
@user_passes_test(is_doctor)
def patient_form(request):
    return render(request,'doctor/patient_form.html')




#####Patient View Methods 
@login_required(login_url='patient/login')
@user_passes_test(is_patient)
def dashboard_patient_view(request):
    return render(request,'patient/dashboard_patient.html')