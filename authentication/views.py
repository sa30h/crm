from django.shortcuts import render,redirect
from .models import *
from django.views import generic
from django.urls import reverse_lazy
from .models import User,EmployeeProfile
from django.contrib.auth import authenticate,login,get_user_model,logout
from rest_framework import generics
from rest_framework.response import Response
from django.contrib import messages


from .forms import *
from django.http import HttpResponse
from .serializers import RegisterApiSerializer,LoginSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin
from ProjectManagement.models import Project 
from django.db.models import Q
import json
from django.core.mail import send_mail
from django.conf import settings
from datetime import date
from ProjectManagement.models import *
from finance.models import *
from services.models import *



#Sa30 Auth api
class RegisterApiView(GenericAPIView,ListModelMixin,CreateModelMixin):
    queryset=User.objects.all()
    serializer_class=RegisterApiSerializer

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class LoginWithTokenAuthenticationAPIView(GenericAPIView):
    queryset= User.objects.all()
    serializer_class    =       LoginSerializer
    permission_classes     =   []
    authentication_classes =   []

    def post(self,request):
        email    =   request.data.get('email')
        password    =   request.data.get('password')
        print('email',email)
        print('password',password)
        # user        =   User.objects.get(email=str(email))
        user          =   authenticate(email=email,password=password)
        print(user)
        if user is not None:
            # login(user,request)
            #TOKEN STUFF
            token, _ = Token.objects.get_or_create(user = user)
            login(request,user)
            #token_expire_handler will check, if the token is expired it will generate new one
            # is_expired, token = token_expire_handler(token)     # The implementation will be described further

            return Response({ 
                'token': token.key,
                'id':user.id,
            } )
        response = {
        "data": {
            "message": "Your login information is invalid",
            "status": "invalid"
        }
    }
        return Response(response)





#################################################### F R O N T    E N D   VIEWS ##################

# sa30 views
def registraiton_view(request):
    context={}
    if request.user.is_admin:
        accounts=User.objects.all().order_by('email')
        print(accounts)
        if request.GET:
            query=request.GET['q']
            context['query']=str(query)
            accounts=User.objects.filter(Q(firstname__icontains=query) | Q(position__icontains=query) ).order_by('position')
            context['accounts']=accounts
            return render(request,'authentication/registration.html',context)


        if request.method=="POST":
            form=RegistratinForm(request.POST)
            if form.is_valid():
                user=form.save(commit=False)
                user.firstname=request.POST['first_name']
                user.save()
                print(user.firstname)
                # email=form.cleaned_data.get('email')
                # raw_password=form.cleaned_data.get('password1')
                # account=authenticate(email=email,password=raw_password)
                # login(request,account)
                context['accounts']=accounts
                return render(request,'authentication/registration.html',context)

            else:
                context['accounts']=accounts
                context['form']=form
        else:
            form=RegistratinForm()
            context['form']=form
            context['accounts']=accounts
        return render(request,'authentication/registration.html',context)
    else:
        return redirect('userlogin')

def position_view(request):
    context={}
    if request.user.is_admin:
        position=Position.objects.all()
        if request.method=="POST":
            form=PositionForm(request.POST)
            if form.is_valid():
                form.save()
                context['position']=position
                return redirect('position')

            else:
                context['position']=position
                context['form']=form
        else:
            form=PositionForm()
            context['form']=form
            context['position']=position
        return render(request,'authentication/position.html',context)
    else:
        return redirect('userlogin')

def positiondelete_view(request,id):
    if request.user.is_admin:

        pi=Position.objects.get(pk=id)
        pi.delete()
        messages.success(request,"successful")
        return redirect('position')
    else:
        messages.success(request,"You don't have delete contact person permission")
        return redirect('position')

def userLogout_view(request):
    logout(request)
    return redirect('home')


def userLogin_view(request):
    context={}

    user=request.user
    if user.is_authenticated:
        return redirect("home")

    if request.method=='POST':
        form=UserLoginForm(request.POST)
        if form.is_valid():
            email=request.POST['email']
            password=request.POST['password']
            user=authenticate(email=email,password=password)
            if user:
                login(request,user)
                return redirect('userdashboard')
    else:
        form=UserLoginForm()
    context['login_form']=form
    return render(request,'authentication/login.html',context)


def userdashboard_view(request):
    context={}
    query=" "
    if request.GET:
        query=request.GET['q']
        context['query']=str(query)
        project=Project.objects.filter(Q(project_name=query) | Q(project_name__icontains=query) | Q(client_company_name__company_Name=query)| Q(client_company_name__company_Name__icontains=query)).order_by('project_name')

        contactperson=ContactPerson.objects.filter(Q(contact_name=query) | Q(contact_name__icontains=query) | Q(company_name__company_Name=query) | Q(company_name__company_Name__icontains=query) ).order_by('contact_name')

        company=company=Company.objects.filter(Q(company_Name__icontains=query) ).order_by('company_Name')

        context['company']=company 
        context['project']=project
        context['person']=contactperson
        return render(request,'authentication/userdashboard.html',context)

    contactperson=ContactPerson.objects.all().order_by('contact_name')
    company=Company.objects.all().order_by('company_Name')
    project=Project.objects.all().order_by('project_name')
    context['person']=contactperson
    context['company']=company
    context['project']=project

    context['totalprojectnumber']=Project.objects.all().count()
    context['inprogressprojectnumber']=Project.objects.filter(project_complete_or_Inprogress='inprogress').count()
    context['completeprojectnumber']=Project.objects.filter(project_complete_or_Inprogress='completed').count()
    context['totalcompanynumber']=Company.objects.all().count()
    context['totalinvoicenumber']=Invoice.objects.all().count()
    context['totalponumber']=PurchaseOrder.objects.all().count()
    context['totalaccountnumber']=User.objects.all().count()
    allposition=Position.objects.all()
    alldepartment=Department.objects.all()
    allbusiness=Business.objects.all()
    accountswithposition=[]
    accountswithdepartment=[]
    projectwithbusiness=[]
    for item in allposition:
        positionaccounts=User.objects.filter(position__position=item).count()
        accountswithposition.append({'position':item,'accounts':positionaccounts})
    context['accountswithposition']=accountswithposition

    for item in alldepartment:
        departmentaccounts=User.objects.filter(department__department_name=item).count()
        accountswithdepartment.append({'department':item,'accounts':departmentaccounts})
    context['accountswithdepartment']=accountswithdepartment

    for item in allbusiness:
        businessproject=Project.objects.filter(business__business_name=item).count()
        projectwithbusiness.append({'business':item,'project':businessproject,'owner':item.business_owner})
    context['projectwithbusiness']=projectwithbusiness
    print(projectwithbusiness)




   

    return render(request,'authentication/userdashboard.html',context)

def get_dashboard_queryset(query=None):
    queryset=[]
    queries=query.split(" ")
    for q in queries:
        company=Company.objects.filter(
            Q(company_Name__icontains=q) 

            ).distinct()        


        for company in company:
            queryset.append(company)


    return list(set(queryset))

def contactperson_view(request,id):
    context ={}
    contactperson=ContactPerson.objects.get(id=id)
    context['person']=contactperson
    return render(request,'authentication/contactpersoninfo.html',context)

def addcontactperson(request):
    if request.user.contactperson_create_permission:
        context={}
        if request.method=='POST':
            form=ContactPersonCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('userdashboard')

        form=ContactPersonCreationForm()
        context['form']=form
        return render(request,'authentication/addcontactperson.html',context)
    else:
        messages.success(request,"You don't have add contact person permission")
        return redirect('userdashboard')

def contactpersondelete(request,id):
    if request.user.contactperson_delete_permission:

        pi=ContactPerson.objects.get(pk=id)
        pi.delete()
        messages.success(request,"successful")
        return redirect('userdashboard')
    else:
        messages.success(request,"You don't have delete contact person permission")
        return redirect('userdashboard')



def contactpersonupdate(request,id): 
    if request.user.contactperson_edit_permission:

        if request.method=="POST":
            pi=ContactPerson.objects.get(pk=id)
            form=ContactPersonCreationForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request,"successful")
                return redirect('userdashboard')

        pi=ContactPerson.objects.get(pk=id)
        form=ContactPersonCreationForm(instance=pi)
        return render(request,'authentication/updatecompany.html',{'form':form})
    else:
        messages.success(request,"You don't have update contact person permission")
        return redirect('userdashboard')

def department_view(request):
    context={}
    if request.user.is_admin:
        department=Department.objects.all()
        if request.method=="POST":
            form=DepartmentForm(request.POST)
            if form.is_valid():
                form.save()
                context['department']=department
                return redirect('department')

            else:
                context['department']=department
                context['form']=form
        else:
            form=DepartmentForm()
            context['form']=form
            context['department']=department
        return render(request,'authentication/department.html',context)
    else:
        return redirect('userlogin')

def departmentdelete_view(request,id):
    if request.user.is_admin:

        pi=Department.objects.get(pk=id)
        pi.delete()
        messages.success(request,"successful")
        return redirect('department')
    else:
        messages.success(request,"You don't have delete contact person permission")
        return redirect('department')

def business_view(request):
    context={}
    if request.user.is_admin:
        business=Business.objects.all()
        if request.method=="POST":
            form=BusinessForm(request.POST)
            if form.is_valid():
                form.save()
                context['business']=business
                return redirect('business')

            else:
                context['business']=business
                context['form']=form
        else:
            form=BusinessForm()
            context['form']=form
            context['business']=business
        return render(request,'authentication/business.html',context)
    else:
        return redirect('userlogin')

def businessdelete_view(request,id):
    if request.user.is_admin:

        pi=Business.objects.get(pk=id)
        pi.delete()
        messages.success(request,"successful")
        return redirect('business')
    else:
        messages.success(request,"You don't have delete contact person permission")
        return redirect('business')


def calenderview(request):
    context={}
    dates=[]
    project=Project.objects.all()
    today = date.today()
    for item in project:

        yearStart=str(item.start_date).split('-')[0]
        monthStart=str(item.start_date).split('-')[1]
        dayStart=str(item.start_date).split('-')[2]
        year=str(item.project_deadline).split('-')[0]
        month=str(item.project_deadline).split('-')[1]
        day=str(item.project_deadline).split('-')[2]
        reminder_note=str(item.reminder_note)
        responsible_person=str(item.responsible_person)
        project_name=item.project_name
        reminder_date=item.reminder
        ide=item.id

        dates.append({"project":item.project_name,"year":year,"month":month,"day":day,"yearStart":yearStart,"monthStart":monthStart,"dayStart":dayStart,"id":ide})
        # reminder_sent=False

        #send mail 
        # if item.reminder==today :
        #     try:
        #         send_mail("{project} reminder".format(project=project_name),
        #         reminder_note,
        #         settings.EMAIL_HOST_USER,
        #         [responsible_person]
        #         )
        #         reminder_sent=True
        #     except Exception as e:
        #         print('Project reminder email not sent.')

     



    return render(request,'authentication/calender/calenderview.html',{'dates':json.dumps(dates)})

def userScorecard(request):
    context={}
    label=[]
    data=[]   

    position=Position.objects.all()
    for item in position:

        data.append(User.objects.filter(position__position=item.position).count())
        label.append(item.position)

    context['positions']=label
    context['data']=data

    Projectlabel=[]
    Projectdata=[]
    inprogress=Project.objects.filter(project_complete_or_Inprogress='inprogress').count()
    completed=Project.objects.filter(project_complete_or_Inprogress='completed').count()
    Projectlabel.append('Inprogress')
    Projectlabel.append('Completed')
    Projectdata.append(inprogress)
    Projectdata.append(completed)
    context['Projectdata']=Projectdata
    context['Projectlabel']=Projectlabel



    return render(request,'authentication/usersScorecard.html',context)

# def contactpersoninfo_view(request,id):
#     context {={}
#     contactperson=ContactPerson.objects.get(id=id)
#     context['person']=contactperson
#     return render(request,'authentication/contactpersoninfo.html',context)

#     return render(request,'authentication/addcompany.html',context)

# def compinfo(request,pk):
#     context={}
#     company = Company.objects.get(id=pk)
#     contactperson=ContactPerson.objects.filter(company_name__company_Name=company.company_Name)
#     project=Project.objects.filter(client_company_name__company_Name=company.company_Name)
#     context['company']=company
#     context['person']=contactperson
#     context['project']=project

#     # print(contactperson)
#     return render(request,'profile/compinfo.html',context)









#sa30

# def register(request):
#     form = CustomUserCreationForm()
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('sign-in')
    
#     context = {'form':form}
#     return render(request,'profile/register.html',context)
    

# def login(request):
#     context = {}
#     return render(request,'profile/login.html',context)

def profile(request):
    return render(request,'profile/dashboard.html')

def customer(request):
    context={}
    customers = Customer.objects.all()
    if request.method=="POST":
        form=CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customers')
    form=CustomerForm()
    context['customers']=customers
    context['form']=form
    return render(request,'authentication/customer.html',context)

def customerdelete_view(request,id):
    if request.user.is_admin:

        pi=Customer.objects.get(pk=id)
        pi.delete()
        messages.success(request,"successful")
        return redirect('customers')
    else:
        messages.success(request,"You don't have delete contact person permission")
        return redirect('customers')


def customerdetail(request,id):
    context={}

    customer = Customer.objects.get(id=id)
    complaint=Complaint.objects.filter(Q(complaint_by__first_name__icontains=customer.first_name))
    context['complaint']=complaint
    context['customer']=customer
    return render(request,'authentication/customerdetail.html',context)
    
def customerinfo(request,pk):
    customer = Customer.objects.get(id=pk)
    return render(request,'profile/custinfo.html',{'customer':customer})


def company(request):
    companies = Company.objects.all()
    context ={'companies':companies}
    return render(request,'profile/company.html',context)

def addcompany(request):
    if request.user.company_create_permission:

        context={}
        if request.method=="POST":
            form=CompanyCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('userdashboard')
        form=CompanyCreationForm()
        context['form']=form
        return render(request,'authentication/addcompany.html',context)
    else:
        messages.info(request,"You don't have add company permission")
        return redirect('userdashboard')

def compinfo(request,pk):
    context={}
    company = Company.objects.get(id=pk)
    contactperson=ContactPerson.objects.filter(company_name__company_Name=company.company_Name)
    project=Project.objects.filter(client_company_name__company_Name=company.company_Name)
    context['company']=company
    context['person']=contactperson
    context['project']=project

    # print(contactperson)
    return render(request,'profile/compinfo.html',context)



def compdelete(request,id):
    if request.user.company_delete_permission:

        pi=Company.objects.get(pk=id)
        pi.delete()
        messages.success(request,"successful")
        return redirect('userdashboard')
    else:
        messages.info(request,"You don't have delete company permission")
        return redirect('userdashboard')


def compupdate(request,id):
    if request.user.company_edit_permission:

        if request.method=="POST":
            pi=Company.objects.get(pk=id)
            form=CompanyCreationForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request,"successful")
                return redirect('userdashboard')

        pi=Company.objects.get(pk=id)
        form=CompanyCreationForm(instance=pi)
        return render(request,'authentication/updatecompany.html',{'form':form})
    else:
        messages.info(request,"You don't have update company permission")
        return redirect('userdashboard')



def employee(request):
    employees = EmployeeProfile.objects.all()
    context ={'employees':employees}
    return render(request,'profile/employee.html',context)
    
def empinfo(request,pk):
    employee = EmployeeProfile.objects.get(id=pk)
    return render(request,'profile/empinfo.html',{'employee':employee})


def vendor(request):
    vendors = Vendor.objects.all()
    context ={'vendors':vendors}
    return render(request,'profile/vendor.html',context)

def vendinfo(request,pk):
    vendor = Vendor.objects.get(id=pk)
    return render(request,'profile/vendinfo.html',{'vendor':vendor})



def finance(request):
    return render(request,'finance/dashboard.html')

def hr(request):
    return render(request,'hr/dashboard.html')

def payroll(request):
    return render(request,'payroll/dashboard.html')

def project(request):
    return render(request,'project/dashboard.html')


def sla(request):
    return render(request,'sla/dashboard.html')


class indexview(generic.ListView):
    template_name = 'profile/index.html'
    context_object_name = 'all_users'

    def get_queryset(self):
        return User.objects.all()

class detailsview(generic.DetailView):
    model = User
    template_name = 'profile/details.html'


class usercreate(generic.CreateView):
    model = User
    fields = '__all__'

class userupdate(generic.UpdateView):
    model = User
    fields = '__all__'

class userdelete(generic.DeleteView):
    model = User
    success_url = reverse_lazy('index')





