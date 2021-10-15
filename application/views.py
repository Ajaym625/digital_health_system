from django.http.response import HttpResponseServerError, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json,re
from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse
from networkx.generators import directed
from networkx.linalg.attrmatrix import _node_value
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
from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from pathlib import Path
import csv 

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')
import networkx as nx
import pandas as pd 
import operator
import numpy as np
# %matplotlib inline



TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates")'
)

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None
    
class ViewPDF(View):
	def get(self, request, *args, **kwargs):
		pdf = render_to_pdf('doctor/anamnesi_pdf.html', request.session.get('post_data'))
		return HttpResponse(pdf, content_type='application/pdf')



#Automaticly downloads to PDF file
class DownloadPDF(View):
	def get(self, request, *args, **kwargs):
		pdf = render_to_pdf('doctor/anamnesi_pdf.html', request.session.get('post_data'))
		response = HttpResponse(pdf, content_type='application/pdf')
		filename = "anamnesi_personale_%s.pdf" %request.session.get('pid')
		content = "attachment; filename='%s'" %(filename)
		response['Content-Disposition'] = content
		return response

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
            messages.success(request, 'Doctor account hsb been created Successfully')
        else:
            messages.info(request,userForm.errors)
            messages.info(request,doctorForm.errors)
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
            patient.doctor_id = None 
            patient=patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
            messages.success(request, 'Patient account has been created Successfully')
        else:
            messages.info(request,userForm.errors)
            messages.info(request,patientForm.errors)
        return HttpResponseRedirect('/patient/login/')
    return render(request,'patient/patient_register.html',context=mydict)


#User Group
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()
def is_admin(user):
    return user.is_superuser


#after login 
def post_login_view(request):
    if is_doctor(request.user):
        return redirect('dashboard_doctor')
        
    elif is_patient(request.user):
        return redirect('dashboard_patient')
    
    elif is_admin(request.user):
        return redirect('administrator')


@login_required(login_url='doctor/login')
@user_passes_test(is_patient)
def patient_pdf(request):
    patient=models.Patient.objects.only('id').get(user_id=request.user.id).id
    file = Path("media/files/anamnesi_personale_"+str(patient)+".pdf")
    if file.is_file():
        return HttpResponseRedirect('http://127.0.0.1:8000/media/files/anamnesi_personale_'+str(patient)+'.pdf')
    else:
        return render(request,'home/404.html') 

@login_required(login_url='doctor/login')
@user_passes_test(is_doctor)
def patient_pdf_doc(request):
    pid=request.GET.get('pid',None)
    # print(pid)
    file = Path("media/files/anamnesi_personale_"+str(pid)+".pdf")
    print(file)
    if file.is_file():
        return HttpResponseRedirect('http://127.0.0.1:8000/media/files/anamnesi_personale_'+str(pid)+'.pdf')
    else:
        return render(request,'home/404.html') 


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

    patient_id = request.GET.get('pid', None)
    patient_name = request.GET.get('pname', None) 
    # print( patient_id, patient_name)
    return render(request,'doctor/patient_form.html',{'p_id':patient_id, 'p_name':patient_name})


@csrf_exempt
@login_required(login_url='/doctor/login')
@user_passes_test(is_doctor)
def anamnesi_personale(request):
    patient_id = request.GET.get('pid', None)
    patient_name = request.GET.get('pname', None) 
    if request.method=='POST':
        post_data = json.loads(request.body.decode("utf-8"))    
        request.session['post_data'] = post_data
    return render(request,'doctor/anamnesi_personale.html',{'p_id':patient_id, 'p_name':patient_name})



@login_required(login_url='/doctor/login')
@user_passes_test(is_doctor)
def form_pdf(request):   
    patient_id = request.GET.get('p_id', None)
    request.session['pid']=patient_id
    context = {'p_id': patient_id}
    return render(request, 'doctor/form_pdf.html', context)



@login_required(login_url='/doctor/login')
@user_passes_test(is_doctor)
def upload_pdf(request):
    patient_id = request.POST.get('p_id')
    patient=models.Patient.objects.get(id=patient_id)
    if request.method == 'POST':
        patient.anamnesi_personale = request.FILES['file']
        patient.save()
    return render(request,'doctor/dashboard_doctor.html')



#####Patient View Methods 
@login_required(login_url='patient/login')
@user_passes_test(is_patient)
def dashboard_patient_view(request):
    return render(request,'patient/dashboard_patient.html')


##########Administrator View Methods 

@login_required(login_url='admin/?next=/administrator')
@user_passes_test(is_admin)
def administrator(request):
    return render(request,'admin/admin_view.html')


@login_required(login_url='admin/?next=/administrator')
@user_passes_test(is_admin)
def dataset(request):
    return render(request,'admin/upload_dataset.html')


@login_required(login_url='admin/?next=/administrator')
@user_passes_test(is_admin)
def upload_dataset(request):
    if request.method == 'POST':
        csv_file = request.FILES["csv_upload"]
        if not csv_file.name.endswith('.csv'):
            messages.warning(request,'The wrong file type was uploaded')
            return HttpResponseRedirect(request.path_info) 

        file_data = csv_file.read().decode("ISO-8859-1")
        csv_data = re.split('\n', file_data)

        for x in csv_data:
            fields = x.split(";")
            try:
                created = models.dataset.objects.update_or_create(
                    codice_patologia = fields[0],
                    patologia = fields[1],
                    codice_sintomo = fields[2],
                    sintomo = fields[3],
                    sintomo_principale = fields[4],
                )
    
            except IndexError:
                pass
        return HttpResponseRedirect('administrator')
    form = forms.dataset()
    data = {'form':form}
    return HttpResponseRedirect('administrator',data)



@login_required(login_url='admin/?next=/administrator')
@user_passes_test(is_admin)
def view_dataset(request):
    dataset = models.dataset.objects.all().exclude(id=1).order_by('id')
    context = {'dataset': dataset}
    return render(request,'admin/dataset_view.html',context)



@login_required(login_url='admin/?next=/administrator')
@user_passes_test(is_admin)
def add_dataset(request):
    return render(request,'admin/add_dataset.html')



@login_required(login_url='admin/?next=/administrator')
@user_passes_test(is_admin)
def add_to_dataset(request):
    if request.method == 'POST':
        add =  models.dataset.objects.update_or_create(
                    codice_patologia = request.POST.get('codice_patologia'),
                    patologia = request.POST.get('patologia'),
                    codice_sintomo = request.POST.get('codice_sintomo'),
                    sintomo = request.POST.get('sintomo'),
                    sintomo_principale = request.POST.get('sintomo_principale'),
                )
        return HttpResponseRedirect('view_dataset')



@login_required(login_url='admin/?next=/administrator')
@user_passes_test(is_admin)
def edit_dataset(request):
    data_id = request.GET.get('id', None)
    data = models.dataset.objects.filter(id=data_id)
    print(data)
    context = {'data': data}
    return render(request,'admin/edit_dataset.html',context)



@login_required(login_url='admin/?next=/administrator')
@user_passes_test(is_admin)
def update_dataset(request):
    dataset_id = request.GET.get('id',None)
    add =  models.dataset.objects.get(id=dataset_id)
    if request.method == 'POST':
        add.codice_patologia = request.POST.get('codice_patologia')
        add.patologia = request.POST.get('patologia')
        add.codice_sintomo = request.POST.get('codice_sintomo')
        add.sintomo = request.POST.get('sintomo')
        add.sintomo_principale = request.POST.get('sintomo_principale')
        add.save()
        return HttpResponseRedirect('view_dataset')



@login_required(login_url='admin/?next=/administrator')
@user_passes_test(is_admin)
def delete_dataset(request):
    dataset_id = request.GET.get('id',None)
    models.dataset.objects.get(id=dataset_id).delete()
    return HttpResponseRedirect('view_dataset')



@login_required(login_url='/doctor/login')
@user_passes_test(is_doctor)
def diagnosis_form(request):
    dataset = models.dataset.objects.all().exclude(id=1).order_by('id')
    context={'dataset': dataset}
    return render(request, 'doctor/diagnosis_form.html',context)


@login_required(login_url='/doctor/login')
@user_passes_test(is_doctor)
def auto_diagnosis(request):
    if request.method == 'POST':
        selected_id = request.POST.getlist('input')

        input=[]
        output=[]
        weights=[]
        selected_symptom=[]

        for id in selected_id:
            query = models.dataset.objects.get(codice_sintomo=id)
            input.append(query.sintomo)
            selected_symptom.append(query.codice_sintomo)
            output.append(query.patologia)
            weights.append(query.sintomo_principale.strip())
       
        input_node= {k: v for v,k in enumerate(input)}
        
        Graph = nx.DiGraph()
        for i in enumerate(output):
            Graph.add_edge(selected_symptom[i[0]], output[i[0]],weight=weights[i[0]])


        so = pd.DataFrame({
            "source": input, 
            "target": output,
            "w": weights,
            'sy': selected_symptom,
            })
        # G=nx.DiGraph(directed=true)
        G=nx.from_pandas_edgelist(so, source="source", target="target", edge_attr="w",create_using=nx.DiGraph())
        
        # print(so["sy"].values)
        # print(forW)
        colors=[]
        target=[]

        for node in G:
                if node in so["target"].values:
                    colors.append("red")
                    target.append(node)
                else:
                    colors.append("lightgreen")
        
        tar = {k: v for v, k in enumerate(target)}
        
        plt.figure(2,figsize=(8,6),dpi=100) 
        plt.text(-0.1,1,tar,fontsize=10,color='red')
        
        # print(tar)
        pos = nx.drawing.layout.circular_layout(G)
       
        nx.draw_networkx_nodes(G, pos=pos, )
        nx.draw_networkx_edges(G, pos=pos,arrows=True, label="w",)
        nx.draw_networkx_labels(G,pos=pos, labels={n:lab for n,lab in input_node.items() if n in pos})
        nx.draw_networkx_labels(G,pos=pos, labels={n:lab for n,lab in tar.items() if n in pos})
        nx.draw_networkx_edge_labels(G, pos=pos);
        
        fig1 = plt.gcf()
        plt.draw()
        plt.figure(2,figsize=(12,11),dpi=100) 
        fig1.savefig("media/graph/graph.png", format="PNG")
        plt.cla()



      
        node={}
        node_weight={}

        array_counter=0
        for symptop in selected_symptom:
            selected_node=symptop
 
            neighbor=list(nx.neighbors(Graph,selected_node))
            node[symptop] = neighbor   
            neighbor_weight=[]
            for elem in neighbor:
                single_weight=(Graph.get_edge_data(selected_node,elem))
                neighbor_weight=neighbor_weight + list(single_weight.values())
                node_weight[symptop] = neighbor_weight
                array_counter=array_counter+1
    
        # print(node)
        # print(node_weight) 

        occurrences = {}
        node_and_weights={}
        for symptop in selected_symptom:
            for s, el in enumerate(node[symptop]):
                if el in occurrences.keys():
                    occurrences[el] += 1
                else:
                    occurrences[el] = 1
                if el in node_and_weights.keys():
                    node_and_weights[el]  +=  int(node_weight[symptop][s])
                else:
                    node_and_weights[el] = int(node_weight[symptop][s])

        # print(occurrences.items())
        # print(weights)

        sortedDict = dict(sorted(node_and_weights.items(),reverse=True, key=operator.itemgetter(1)))
        context = {'sortedDict': sortedDict}
        return render(request, 'doctor/diagnosis_output.html',context)


@login_required(login_url='admin/?next=/administrator')
@user_passes_test(is_admin)
def visualize_graph(request):
    dataset = models.dataset.objects.all().exclude(id=1).order_by('id')
    # print(dataset)
    input=[]
    output=[]
    weights=[]
    selected_symptom=[]
    codice_sintomo=[]
    for id in dataset:
        input.append(id.sintomo)
        selected_symptom.append(id.codice_sintomo)
        output.append(id.patologia)
        weights.append(id.sintomo_principale.strip())
    # print(weights)
    # print(input)
    input_node= {k: v for v, k in enumerate(input)}
    # print(id1)
    so = pd.DataFrame({
    "source": input, 
    "target": output,
    "w": weights,
    })

    G = nx.from_pandas_edgelist(so, source="source", target="target", edge_attr="w")

    colors=[]
    target=[]

    for node in G:
        if node in so["target"].values:
            colors.append("red")
            target.append(node)
        else:
            colors.append("lightgreen")
    tar = {k: v for v, k in enumerate(target)}

    plt.figure(2,figsize=(32,15),dpi=100) 
    plt.text(-0.6,0.5,tar,fontsize=36,color='red')
    
    
    random_pos = nx.random_layout(G, seed=22)
    pos = nx.spring_layout(G, dim=2, k=None, pos=random_pos, fixed=None, iterations=50, weight='w', scale=1.0)
    # plt.savefig("media/graph/dataset_graph.png", bbox_inches = 'tight')
    nx.draw_networkx_nodes(G, pos=pos,  node_color=colors, node_size=1000)
    nx.draw_networkx_edges(G, pos=pos, edge_cmap=plt.cm.viridis, edge_vmin=0, width=1)
    nx.draw_networkx_labels(G, pos=pos, labels={n:lab for n,lab in input_node.items() if n in pos}, font_size=12, font_color='k', font_family='sans-serif', font_weight='normal', alpha=None, bbox=None, horizontalalignment='center', verticalalignment='center', ax=None)
    nx.draw_networkx_labels(G,pos=pos, labels={n:lab for n,lab in tar.items() if n in pos})
    nx.draw_networkx_edge_labels(G, pos=pos);

    
    
    # fig1 = plt.gcf()
    plt.draw()
    plt.savefig("media/graph/dataset_graph.png", format="PNG", bbox_inches = 'tight')
    
    plt.cla()
    return HttpResponseRedirect('http://localhost:8000/media/graph/dataset_graph.png')
    # return render(request,'admin/dataset_view.html')