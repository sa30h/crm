from django.urls import path
from . import views
from .api import *
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    
    
    path('',views.profile,name = 'profile'),

    # sa30 Api
    path('registerApi/',views.RegisterApiView.as_view()),
    path('loginApi/',views.LoginWithTokenAuthenticationAPIView.as_view()),
    #sa30 Api
    path('register/',views.registraiton_view,name="register"),
    path('position/',views.position_view,name="position"),
    path('positiondelete/<int:id>',views.positiondelete_view,name="positiondelete"),
    path('department/',views.department_view,name="department"),
    path('departmentdelete/<int:id>',views.departmentdelete_view,name="departmentdelete"),
    path('business/',views.business_view,name="business"),
    path('businessdelete/<int:id>',views.businessdelete_view,name="businessdelete"),
    path('login/',views.userLogin_view,name="userlogin"),
    path('logout/',views.userLogout_view,name="userlogout"),
    path('dashboard/',views.userdashboard_view,name="userdashboard"),
    path('addcompany/',views.addcompany,name="addcompany"),
    path('company/<int:pk>',views.compinfo,name="companyinfo"),
    path('companyupdate/<int:id>',views.compupdate,name="companyupdate"),
    path('companydelete/<int:id>',views.compdelete,name="companydelete"),
    path('contactperson/<int:id>',views.contactperson_view,name="contactperson"),
    path('addcontactperson/',views.addcontactperson,name="addcontactperson"),
    path('contactpersonupdate/<int:id>',views.contactpersonupdate,name="contactpersonupdate"),
    path('contactpersondelete/<int:id>',views.contactpersondelete,name="contactpersondelete"),
    path('calenderview/',views.calenderview,name="calenderview"),
    path('userScorecard/',views.userScorecard,name="userScorecard"),

    


    
    # authentication/
    path('user/', views.indexview.as_view(), name = 'user'),

    path('customer/', views.customer, name = 'customers'),
    path('customer/<pk>/', views.customerinfo, name = 'customerinfo'),
    path('customerdelete/<id>/', views.customerdelete_view, name = 'customerdelete'),
    path('customerdetail/<id>/', views.customerdetail, name = 'customerdetail'),


    path('company/', views.company, name = 'company'),
    path('company/<pk>/', views.compinfo, name = 'compinfo'),

    path('employee/', views.employee, name = 'employee'),
    path('employee/<pk>', views.empinfo, name = 'empinfo'),

    path('vendor/', views.vendor, name = 'vendor'),
    path('vendor/<pk>', views.vendinfo, name = 'vendinfo'),


    
    # path('register/', views.register, name='sign-up'),
    # path('login/', views.login, name='sign-in'),


]
    
    
 


