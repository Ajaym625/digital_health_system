from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView


urlpatterns = [  
    path('',views.index  ,name='index'), 
    path('admin/', admin.site.urls, name='admin'  ),
    
    path('doctor/', views.doctor_landing,name='doctor_landing'), 
    path('patient/',views.patient_landing,name='patient_landing'),
    
    path('doctor/login/', LoginView.as_view(template_name='doctor/doctor_login.html')),
    path('doctor/register/',views.doctor_register, name='doctor_register'),

    path('patient/login/',LoginView.as_view(template_name='patient/patient_login.html')), 
    path('patient/register/',views.patient_register, name='patient_register'),

    path('post_login', views.post_login_view,name='post_login'),
    path('logout', LogoutView.as_view(template_name='home/index.html'),name='logout'),

    path('dashboard_doctor', views.dashboard_doctor_view,name='dashboard_doctor'),  
    path('dashboard_patient', views.dashboard_patient_view,name='dashboard_patient'), 

    path('doctor/patient_list', views.patient_list,name='patient_list'),
    path('doctor/patient_selection',views.patient_selection,name='patient_selection'),
    path('doctor/visualize_patient',views.visualize_patient,name='visualize_patient'),
    path('doctor/patient_form',views.patient_form,name='patient_form'),
] 