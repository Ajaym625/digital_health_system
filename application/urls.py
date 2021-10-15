from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [  
    path('',views.index  ,name='index'), 
    # path('admin/', admin.site.urls, name='admin'  ),
    
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
    path('doctor/anamnesi_personale',views.anamnesi_personale,name='anamnesi_personale'),

    path('doctor/form_pdf/',views.form_pdf,name='form_pdf'),
    path('pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
    path('pdf_download/', views.DownloadPDF.as_view(), name="pdf_download"),
    path('upload_pdf/', views.upload_pdf, name="upload_pdf"),

    path('patient_pdf', views.patient_pdf,name='patient_pdf'),
    path('patient_pdf_doc', views.patient_pdf_doc,name='patient_pdf_doc'),


    path('administrator',views.administrator,name='administrator'),
    path('dataset', views.dataset,name='dataset'),
    path('upload_dataset', views.upload_dataset,name='upload_dataset'),
    path('view_dataset', views.view_dataset,name='view_dataset'),
    path('add_dataset', views.add_dataset,name='add_dataset'),
    path('add_to_dataset', views.add_to_dataset,name='add_to_dataset'),
    path('edit_dataset', views.edit_dataset,name='edit_dataset'),
    path('update_dataset', views.update_dataset,name='update_dataset'),
    path('delete_dataset', views.delete_dataset,name='delete_dataset'),

    path('doctor/diagnosis_form', views.diagnosis_form,name='diagnosis_form'),
    path('doctor/auto_diagnosis',views.auto_diagnosis,name='auto_diagnosis'),
    path('visualize_graph', views.visualize_graph,name='visualize_graph'),

# path('doctor/anamnesi_personale1',views.anamnesi_personale1,name='anamnesi_personale1'),
    # path('pdf/', views.GeneratePdf.as_view()), 
] 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)