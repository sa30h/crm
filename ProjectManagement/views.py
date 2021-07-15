from django.shortcuts import render
from django.shortcuts import render,redirect

from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics,mixins
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
from rest_framework.authentication import SessionAuthentication
from .models import *
from .serializer import *
from .forms import *
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q
from authentication.models import ContactPerson



# sa30 Project management api view
class CR_ProjectApiView(GenericAPIView,ListModelMixin,CreateModelMixin):
    queryset=Project.objects.all()
    serializer_class=ProjectSerializer
    authentication_classes=[SessionAuthentication]

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def  post(self,request,*args,**kwargs):
        user=self.request.user
        position=user.position
        read=user.read_entries
        create=user.create_entry
        edit=user.edit_entry
        delete=user.edit_entry
        if position=="manager":
            return self.create(request,*args,**kwargs)
        return Response("You have not access")

        
        
        

class U_ProjectApiView(GenericAPIView,UpdateModelMixin,RetrieveModelMixin):
    queryset=Project.objects.all()
    serializer_class=ProjectSerializer
    authentication_classes=[SessionAuthentication]


    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        user=self.request.user
        position=user.position
        read=user.read_entries
        create=user.create_entry
        edit=user.edit_entry
        delete=user.edit_entry
        if position=="manager" :

            return self.update(request,*args,**kwargs)
        response('You dont have access')

class CR_TeamApiView(GenericAPIView,ListModelMixin,CreateModelMixin):
    queryset=Team.objects.all()
    serializer_class=TeamSerializer
    authentication_classes=[SessionAuthentication]

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def  post(self,request,*args,**kwargs):
        user=self.request.user
        position=user.position
        read=user.read_entries
        create=user.create_entry
        edit=user.edit_entry
        delete=user.edit_entry
        if position=="manager":
            return self.create(request,*args,**kwargs)
        response('You dont have access')


class U_TeamApiView(GenericAPIView,UpdateModelMixin,RetrieveModelMixin):
    queryset=Team.objects.all()
    serializer_class=TeamSerializer
    authentication_classes=[SessionAuthentication]

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        user=self.request.user
        position=user.position
        read=user.read_entries
        create=user.create_entry
        edit=user.edit_entry
        delete=user.edit_entry
        if position=="manager":
            return self.create(request,*args,**kwargs)
        response('You dont have access')

class CR_TeamMemberApiView(GenericAPIView,ListModelMixin,CreateModelMixin):
    queryset=TeamMember.objects.all()
    serializer_class=TeamMemberSerializer
    authentication_classes=[SessionAuthentication]


    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def  post(self,request,*args,**kwargs):
        user=self.request.user
        position=user.position
        read=user.read_entries
        create=user.create_entry
        edit=user.edit_entry
        delete=user.edit_entry
        if position=="manager":
            return self.create(request,*args,**kwargs)
        response('You dont have access')

class U_TeamMemberApiView(GenericAPIView,UpdateModelMixin,RetrieveModelMixin):
    queryset=TeamMember.objects.all()
    serializer_class=TeamMemberSerializer
    authentication_classes=[SessionAuthentication]


    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        user=self.request.user
        position=user.position
        read=user.read_entries
        create=user.create_entry
        edit=user.edit_entry
        delete=user.edit_entry
        if position=="manager" :
            return self.create(request,*args,**kwargs)
        response('You dont have access')

class CR_Tasks(GenericAPIView,ListModelMixin,CreateModelMixin):
    queryset=Tasks.objects.all()
    serializer_class=TasksSerializer
    authentication_classes=[SessionAuthentication]

  


    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
  
    def  post(self,request,*args,**kwargs):
        user=self.request.user
        position=user.position
        read=user.read_entries
        create=user.create_entry
        edit=user.edit_entry
        delete=user.edit_entry
        if position=="manager" :
            return self.create(request,*args,**kwargs)
        response('You dont have access')
   

class U_Tasks(GenericAPIView,UpdateModelMixin,RetrieveModelMixin):
    queryset=Tasks.objects.all()
    serializer_class=TasksSerializer
    authentication_classes=[SessionAuthentication]



    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        user=self.request.user
        position=user.position
        read=user.read_entries
        create=user.create_entry
        edit=user.edit_entry
        delete=user.edit_entry
        if position=="manager" :
            return self.create(request,*args,**kwargs)
        response('You dont have access')

def home(request):
    context={}
    project=Project.objects.all().count()
    pending=Project.objects.filter(project_complete_or_Inprogress='inprogress').count()
    completed=Project.objects.filter(project_complete_or_Inprogress='completed').count()

    context['total_project']=project
    context['inprogress_project']=pending
    context['completed']=completed
    return render(request,'ProjectManagement/projectmanagement.html',context)

def project_view(request):
    context={}
    print(request.user.project_create_permission)
    if request.user.company_create_permission:
        if request.method=="POST":
            form=ProjectCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"successful")
                return redirect('projectmanagementHome')

        context['form']=ProjectCreationForm()
        return render(request,'ProjectManagement/project.html',context)
    else:
        messages.info(request,"You don't have create project permission")
        return redirect('projectmanagementHome')

def projectUpdate_view(request,id):
    if request.user.project_edit_permission:
        if request.method=="POST":           
            pi=Project.objects.get(pk=id)
            form=ProjectCreationForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request,"successful")
                return redirect('projectmanagementHome')

        pi=Project.objects.get(pk=id)
        form=ProjectCreationForm(instance=pi)
        return render(request,'ProjectManagement/updateproject.html',{'form':form})
    else:
        messages.info(request,"You don't have update project permission")
        return redirect('projectmanagementHome')

def projectDelete_view(request,id):
    if request.user.project_delete_permission:

        pi=Project.objects.get(pk=id)
        pi.delete()
        messages.success(request,"successful")
        return redirect('projectmanagementHome')
    else:
        messages.info(request,"You don't have delete project permission")
        return redirect('projectmanagementHome')

def totalproject_view(request):
    if request.user.project_read_permission:

        context={}
        project=Project.objects.all()
        context['project']=project
        return render(request,'ProjectManagement/totalprojectView.html',context)
    else:
        messages.info(request,"You don't have View project permission")
        return redirect('projectmanagementHome')

def inprogressproject_view(request):
    if request.user.project_read_permission:

        context={}
        project=Project.objects.filter(project_complete_or_Inprogress='inprogress')
        context['project']=project
        return render(request,'ProjectManagement/inprogressproject.html',context)
    else:
        messages.info(request,"You don't have View project permission")
        return redirect('projectmanagementHome')

def completedproject_view(request):
    if request.user.project_read_permission:

        context={}
        project=Project.objects.filter(project_complete_or_Inprogress='completed')
        context['project']=project
        return render(request,'ProjectManagement/completedproject.html',context)
    else:
        messages.info(request,"You don't have View project permission")
        return redirect('projectmanagementHome')

def team_view(request):
    context={}
    if request.method=="POST":
        form=TeamCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"successful")
            return redirect('projectmanagementHome')
    context['form']=TeamCreationForm()
    return render(request,'ProjectManagement/team.html',context)

def teamView_view(request):
    context={}

    item=Team.objects.all()
    item2=TeamMember.objects.all()

    context['Team']=item
    context['member']=item2
    return render(request,'ProjectManagement/teamView.html',context)

def teamDelete_view(request,id):
    pi=Team.objects.get(pk=id)
    pi.delete()
    messages.success(request,"successful")
    return redirect('projectmanagementHome')


def teamUpdate_view(request,id):
    if request.method=="POST":
        pi=Team.objects.get(pk=id)
        form=TeamCreationForm(request.POST,instance=pi)
        if form.is_valid():
            form.save()
            messages.success(request,"successful")
            return redirect('projectmanagementHome')

    pi=Team.objects.get(pk=id)
    form=TeamCreationForm(instance=pi)
    return render(request,'ProjectManagement/updateTeam.html',{'form':form})
   

def teammember_view(request):
    context={}
    user=request.user
    l1=Team.objects.filter(project_manager=user)
    if l1.count() >0:    
        if request.method=="POST":
            form=TeamMemberCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"successful")
                return redirect('projectmanagementHome')        
        context['form']=TeamMemberCreationForm()
        return render(request,'ProjectManagement/teammember.html',context)
    context['msg']="You don't have access to this page"
    return render(request,'ProjectManagement/projectmanagement.html',context)

def teammemberView_view(request):
    context={}
    user=request.user
    l1=Team.objects.filter(project_manager=user)
    if l1.count() >0:
        item2=TeamMember.objects.all()
        context['member']=item2
        return render(request,'ProjectManagement/teammemberView.html',context)
    context['msg']="You don't have access to this page"
    return render(request,'ProjectManagement/projectmanagement.html',context)

def teammemberDelete_view(request,id):
    pi=TeamMember.objects.get(pk=id)
    pi.delete()
    messages.success(request,"successful")
    return redirect('projectmanagementHome')


def teammemberUpdate_view(request,id):
    user=request.user
    l1=Team.objects.filter(project_manager=user)
    if l1.count() >0:    
        if request.method=="POST":
            pi=TeamMember.objects.get(pk=id)
            form=TeamMemberCreationForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request,"successful")
                return redirect('projectmanagementHome')

        pi=TeamMember.objects.get(pk=id)
        form=TeamMemberCreationForm(instance=pi)
        return render(request,'ProjectManagement/updateTeamMember.html',{'form':form})

    context['msg']="You don't have access to this page"
    return render(request,'ProjectManagement/projectmanagement.html',context)

def tasks_view(request):
    context={}
    user=request.user
    
    if request.method=="POST":  
        form=AllocateTaskForm(request.POST)
        if form.is_valid():
            
            taskk=form.save(commit=False)
            Getteam=request.POST['team']
            fetchteam=Team.objects.get(id=Getteam)
            print(type(fetchteam.project.project_name))
            Getmember=request.POST['member']
            print(Getmember)
            fetchmemberdata=TeamMember.objects.get(id=Getmember)
            print('s',fetchmemberdata.team_member.email)
            fetchmember=TeamMember.objects.filter(Q(team__project__project_name=fetchteam.project.project_name) & Q(team_member__email=fetchmemberdata.team_member.email))
            # fetchmember=TeamMember.objects.filter( Q(team__project__project_name=fetchteam.project.project_name) | Q(team_member__email=fetchmemberdata.team_member.email))

            # fetchmember=TeamMember.objects.get(id=Getteam)
            print('ds',fetchmember)

            taskk.member=fetchmember[0]
            taskk.save()
            messages.success(request,"successful")
            return redirect('projectmanagementHome')

        print(form)
    context['form']=AllocateTaskForm()
    return render(request,'ProjectManagement/task.html',context)

    # context['msg']="You don't have access to this page"
    # return render(request,'ProjectManagement/projectmanagement.html',context)

def addTaskInfoPage(request,membername,teamname):
    context={}
    print('team',teamname)
    context['teamname']=teamname
    member=membername
    context['member']=member
    if request.method=="POST":  
        form=Addtaskinfopage(request.POST)
        if form.is_valid():
            teamdata=Team.objects.filter(project__project_name=teamname)
            memberData=TeamMember.objects.filter(Q(team_member__email=membername) & Q(team__project__project_name=teamname))
            print('memberData',memberData)
            content=form.save(commit=False)
            content.member=memberData[0]
            content.team=teamdata[0]
            content.save()
            messages.success(request,"successful")
            return redirect('userdashboard')

        
    context['form']=Addtaskinfopage()
    return render(request,'ProjectManagement/addtaskinfopage.html',context)

def tasksView_view(request):
    context={}
    user=request.user
    l1=Team.objects.filter(project_manager=user)
    if l1.count() >0:
        item=Tasks.objects.all()
        context['Task']=item
        return render(request,'ProjectManagement/TaskView.html',context)

    context['msg']="You don't have access to this page"
    return render(request,'ProjectManagement/projectmanagement.html',context)

def singletaskstatus(request,id):
    context={}
    task=Tasks.objects.get(id=id)
    context['task']=task
    return render(request,'ProjectManagement/singletaskstatus.html',context)

def singletask_view(request,projectname):
    print(projectname)
    forTask=[]
    context={}
    item=Tasks.objects.filter(member__team__project__project_name=projectname)
    context['Task']=item
    task= Tasks.objects.filter(member__team__project__project_name=projectname)
    for x in task:
        if x.member.team_member.email not in forTask:
            if x.updates == 'allocated':
                color='warning'
            elif x.updates == 'completed':
                color='success'
            elif x.updates == 'error':
                color='danger'
            forTask.append({'member':x.member.team_member.email,'color':color})
    


    print(forTask)
    

    context['taskA']=forTask
    return render(request,'ProjectManagement/singletaskview.html',context)


def tasksDelete_view(request,id):
    pi=Tasks.objects.get(pk=id)
    pi.delete()
    messages.success(request,"successful")
    return redirect('projectmanagementHome')

def taskUpdate_view(request,id):
    user=request.user
    l1=Team.objects.filter(project_manager=user)
    if l1.count() >0:    
        if request.method=="POST":
            pi=Tasks.objects.get(pk=id)
            form=AllocateTaskForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request,"successful")
                return redirect('projectmanagementHome')

        pi=Tasks.objects.get(pk=id)
        form=AllocateTaskForm(instance=pi)
        return render(request,'ProjectManagement/updateTask.html',{'form':form})

    context['msg']="You don't have access to this page"
    return render(request,'ProjectManagement/projectmanagement.html',context)


def taskprogressView_view(request):

    context={}
    user=User.objects.get(email=request.user)
    u=request.user
    item=Tasks.objects.all()
    context['Task']=item
    return render(request,'ProjectManagement/updatetaskprogressView.html',context)

def taskprogressUpdate_view(request,id):
    if request.method=="POST":
        pi=Tasks.objects.get(pk=id)
        form=AllocateTaskForm(request.POST,instance=pi)

        if form.is_valid():
            form.save()
            messages.success(request,"successful")
            return redirect('projectmanagementHome')

    pi=Tasks.objects.get(pk=id)
    form=AllocateTaskForm(instance=pi)
    return render(request,'ProjectManagement/updateprogress.html',{'form':form})

def projectInfo_view(request,id):
    context={}
    forTask=[]
    project=Project.objects.get(pk=id)
    color=''
    team=Team.objects.filter( Q(project__project_name=project.project_name))

    member=TeamMember.objects.filter( Q(team__project__project_name=project.project_name))

    contactPerson=ContactPerson.objects.filter(Q(company_name=project.client_company_name))
    task= Tasks.objects.filter(member__team__project__project_name=project.project_name)
    for x in task:
        if x.member.team_member.email not in forTask:
            if x.updates == 'allocated':
                color='warning'
            elif x.updates == 'completed':
                color='success'
            elif x.updates == 'error':
                color='danger'
            forTask.append({'member':x.member.team_member.email,'color':color,'xx':int(x.id)})
    


    print(forTask)


    context['taskA']=forTask
    context['tasks']=task
    context['project']=project
    context['team']=team
    context['member']=member
    context['contactPerson']=contactPerson

    return render(request,'ProjectManagement/projectinfo.html',context)



#from  django.core.mail import send_mail

# def index (request):
#    send_mail(
#         'followup','concall with amit'+'\nmeeting with rahul','amanpreetleanvia.com',['amanpreet1052@gmail.com'],fail_silently=False)
#    return render(request,'index.html')

######################BusinessDevelopment###############################

class BOListView(generics.ListCreateAPIView):
    # parser_classes = (MultiPartParser, FormParser)

    queryset = Businessopportunity.objects.all()
    serializer_class = BusinessopportunitySerializer


class BOView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BusinessopportunitySerializer
    queryset = Businessopportunity.objects.all()



class ProjectListView(generics.ListCreateAPIView):
    # parser_classes = (MultiPartParser, FormParser)

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()



#class TeamListView(generics.ListCreateAPIView):
 #   queryset = Team.objects.all()
  #  serializer_class = TeamSerializer








#
# class BusinessopportunityList(APIView):
#
#     def get(self,request):
#             queryset               =         Businessopportunity.objects.all()
#             serializer             =          BusinessopportunitySerializer(queryset,many=True)
#             permission_classes     =         []
#             authentication_class   =         []
#             return Response(serializer.data)
#
#
#     def post(self,request):
#             serializer            =      BusinessopportunitySerializer(data=request.data)
#             permission_classes     =      []
#             authentication_class   =      []
#             if serializer.is_valid():
#                     serializer.save()
#                     return Response(serializer.data, status=status.HTTP_201_CREATED)
#             else:
#                 return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    ##no of times hit send = objects created

# class Business_opportunityUpdateAPIView(generics.UpdateAPIView):
#     queryset               =         Business_opportunity.objects.all()
#     serializers_class      =         Business_opportunitySerializer
#     permission_classes     =         []
#     authentication_class   =         []
#     lookup_field           =         'project_name'

###############################Project#################################
#
# class ProjectList(APIView):
#     def get(self,request):
#             queryset               =         Project.objects.all()
#             serializer             =         ProjectSerializer(queryset,many=True)
#             permission_classes     =         []
#             authentication_class   =         []
#             return Response(serializer.data)
#
#     def post(self,request):
#             serializer            =      Business_opportunitySerializer(data=request.data)
#             permission_classes     =      []
#             authentication_class   =      []
#             if serializer.is_valid():
#                     serializer.save()
#                     return Response(serializer.data, status=status.HTTP_201_CREATED)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# # class ProjectUpdateAPIView(generics.UpdateAPIView):
#     queryset               =         Project.objects.all()
#     serializers_class      =         ProjectSerializer
#     permission_classes     =         []
#     authentication_class   =         []
#     lookup_field           =         ''

############################Team#################################

class TeamList(APIView):
        def get(self,request):
                    queryset               =         Team.objects.all()
                    serializer             =         TeamSerializer(queryset,many=True)
                    permission_classes     =         []
                    authentication_class   =         []
                    return Response(serializer.data)

        def post(self, request):
                    serializer             =     TeamSerializer(data=request.data)
                    permission_classes      =     []
                    authentication_class    =     []
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class TeamUpdateAPIView(generics.UpdateAPIView):
#     queryset               =         Team.objects.all()
#     serializers_class      =         TeamSerializer
#     permission_classes     =         []
#     authentication_class   =         []
#     lookup_field           =         ''

# def ProjectManagement(request):
#     return render(request,'project/dashboard.html')