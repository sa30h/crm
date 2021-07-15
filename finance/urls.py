from django.urls import path
from . import views
from . import api

urlpatterns = [
    
    path('',views.financeHome,name='financeHome'),

    path('dashboard/',views.finance,name='finance'),

    # path('invoice/', views.invoice, name = 'invoice'),
    path('invoice/', views.invoice, name = 'invoices'),#addede sa30
    path('invoice/<pk>/', views.invinfo, name = 'invinfo'),
    path('create_invoice/',views.createinvoice,name='create_invoice'),
    path('update_invoice/<pk>/',views.updateinvoice,name='update_invoice'),
    path('update_inent/<pk>/',views.updateSEnt,name='update_inentry'),
    path('delete_invoice/<pk>/',views.deleteinvoice,name='delete_invoice'),
    path('delete_inent/<pk>/',views.deleteSEnt,name='delete_inentry'),


    # po - purchase order
    # path('po/', views.po, name = 'po'),
    path('po/', views.po, name = 'poS'),
    path('po/<pk>/', views.poinfo, name = 'poinfo'),
    path('create_po/',views.createPO,name='create_po'),
    path('update_po/<pk>/',views.updatePO,name='update_po'),
    path('update_poent/<pk>/',views.updatePEnt,name='update_poentry'),
    path('delete_po/<pk>/',views.deletePO,name='delete_po'),
    path('delete_poent/<pk>/',views.deletePEnt,name='delete_poentry'),


]