from django.shortcuts import render,redirect
from .models import *
from services.models import *
from .serializer import InvoiceSerializer,PurchaseOrderSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework import generics,mixins
from services.models import *
from .forms import *
from .filters import *
from django.db.models.signals import pre_save,post_save
from django.db.models import Q
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
from rest_framework.authentication import SessionAuthentication
from .serializer import *



# PurchaseOrderSerializer
# MonthlySalary
class InvoiceApiView(GenericAPIView,ListModelMixin,CreateModelMixin):
    queryset=Invoice.objects.all()
    serializer_class=InvoiceSerializer
    authentication_classes=[SessionAuthentication]
    
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class UD_InvoiceApiView(GenericAPIView,UpdateModelMixin,RetrieveModelMixin,DestroyModelMixin):
    queryset=Invoice.objects.all()
    serializer_class=InvoiceSerializer
    authentication_classes=[SessionAuthentication]



    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)

class PoApiView(GenericAPIView,ListModelMixin,CreateModelMixin):
    queryset=PurchaseOrder.objects.all()
    serializer_class=PurchaseOrderSerializer
    authentication_classes=[SessionAuthentication]
    
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class UD_PoApiView(GenericAPIView,UpdateModelMixin,RetrieveModelMixin,DestroyModelMixin):
    queryset=PurchaseOrder.objects.all()
    serializer_class=PurchaseOrderSerializer
    authentication_classes=[SessionAuthentication]



    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)



def financeHome(request):
    return render(request,'finance1/home.html')


def finance(request):
    return render(request,'finance/dashboard.html')


def invoice(request):
    context={}
    query=" "
    if request.GET:
        query=request.GET['q']
        context['query']=str(query)
        invoices=Invoice.objects.filter(Q(client_company__company_Name=query)| Q(client_company__company_Name__icontains=query) |Q(payment_terms=query) | Q(payment_terms__icontains=query)).order_by('client_company__company_Name')


        context['invoices']=invoices 
        return render(request,'finance/invoice.html',context)

    invoices=Invoice.objects.all().order_by('client_company__company_Name')

    context['invoices']=invoices
 
   

    return render(request,'finance/invoice.html',context)

# def invoice(request):
#     context={}
#     query=" "
#     if request.GET:

#         query=request.GET['q']
#         context['query']=str(query)
#         invoices=Invoice.objects.filter(Q(client_company__company_Name=query) | Q(client_company__company_Name__icontains=query) | Q(Invoice_number=query)| Q(Invoice_number__icontains=query  | Q(payment_terms=query) | Q(payment_terms__icontains=query))

#         context['invoices']=invoices
#         return render(request,'finance/invoice.html',context)

#     invoices = Invoice.objects.all()
#     context['invoices']=invoices
   

#     return render(request,'finance/invoice.html',context)

    # invfilter = InvoiceFilter(request.GET,queryset=invoices)
    # invoices = invfilter.qs

    # context = {'invoices':invoices,}
    # context = {'invoices': invoices, 'invfilter': invfilter}
    # return render(request,'finance/invoice.html',context)


def invinfo(request,pk):
    invoice = Invoice.objects.get(id=pk)
    # entries = invoice.serviceentry_set.all()
    # s = 0
    # for q in entries.iterator():         ############## need to modify , its wrong here
    #     s += (q.rate * q.Qty) - (((q.Discount)/100) * (q.Qty * q.rate)) + q.Tax
    
    
    # context = {'invoice':invoice,'entries':entries} #,'sum': s
    context = {'invoice':invoice} #,'sum': s
    return render(request,'finance/invinfo.html',context)

def createinvoice(request):
    inv_form = InvoiceForm() 
    service_form=ServiceForm()
   
    # ent_form = SEntryForm()
    if request.method == 'POST':
        inv_form = InvoiceForm(request.POST)
        service_form=ServiceForm(request.POST)

        if inv_form.is_valid():
            inv_form.save()
            pre_save.send(sender=Invoice)
            return redirect('invoices')

        # print("inv_form  :" ,inv_form)
        # ent_form = SEntryForm(request.POST)
        # if inv_form.is_valid() and ent_form.is_valid():

        # if inv_form.is_valid() and service_form.is_valid():
        #     service=service_form.save()
        #     invoice=inv_form.save(commit=False)
        #     invoice.service=service
        #     invoice.save()
        # if inv_form.is_valid():
            # inv = inv_form.save()
            # inv.pre_save.connect(pre_save_Stotal, sender=Invoice)
            # ent = ent_form.save(commit=False)


            # ent.invoice = inv
            # ent.save()
        if service_form.is_valid():
            service_form.save()
                # pre_save.send(sender=Invoice)
            return redirect('create_invoice')



    # context = {'inv_form':inv_form,'ent_form':ent_form}
    context = {'inv_form':inv_form,'service_form':service_form}

    return render(request,'finance/invoice_form.html',context)


def updateinvoice(request,pk): # only for updating the invoice,
    invoice = Invoice.objects.get(id=pk)
    # entry = ServiceEntry.objects.get(id=pk)
    inv_form = InvoiceForm(instance=invoice)
    # ent_form = SEntryForm(instance=entry)
    if request.method == 'POST':
        inv_form = InvoiceForm(request.POST,instance=invoice)
        # ent_form = SEntryForm(request.POST,instance=entry)
        if inv_form.is_valid(): #and ent_form.is_valid():
            inv = inv_form.save()
            # ent = ent_form.save(False)

            # ent.invoice = inv
            # ent.save()
            return redirect('invoices')
    context = {'inv_form':inv_form} #,'ent_form':ent_form
    
    return render(request,'finance/updinv_form.html',context)


def updateSEnt(request,pk):  # SERVICE ENTRY
    entry = ServiceEntry.objects.get(id=pk)
    ent_form = SEntryForm(instance=entry)
    if request.method == 'POST':
        ent_form = SEntryForm(request.POST,instance=entry)
        ent = ent_form.save()

        return redirect('invoice')

    context = {'ent_form':ent_form} #,'ent_form':ent_form
    return render(request,'finance/updinvent_form.html',context)


def deleteinvoice(request,pk):
    item = Invoice.objects.get(id=pk)
    if request.method == 'POST':
        item = Invoice.objects.get(id=pk)
        item.delete()
        return redirect('invoices')

    context = {'item':item}
    return render(request,'finance/deleteinv.html',context)

def deleteSEnt(request,pk):
    item = ServiceEntry.objects.get(id=pk)
    # obj = Invoice.objects.get(id=pk)
    if request.method == 'POST':
        item = ServiceEntry.objects.get(id=pk)
        item.delete()
        # obj = Invoice.objects.get(id=pk)
        return redirect('invoice')

    context = {'item':item}
    return render(request,'finance/deleteinv.html',context)



############################################# Below PURCHASE ORDER VIEWS ####################################


# def po(request):
#     pos = PurchaseOrder.objects.all()
#     context = {'pos':pos}
#     return render(request,'finance/po.html',context)

def po(request):
    context={}
    query=" "
    if request.GET:
        query=request.GET['q']
        context['query']=str(query)
        pos=PurchaseOrder.objects.filter(Q(Vendor__company_Name=query)| Q(Vendor__company_Name__icontains=query) ).order_by('Vendor__company_Name')


        context['pos']=pos 
        return render(request,'finance/po.html',context)

    pos=PurchaseOrder.objects.all().order_by('Vendor__company_Name')

    context['pos']=pos
 
   

    return render(request,'finance/po.html',context)



def poinfo(request,pk):
    po = PurchaseOrder.objects.get(id=pk)
    # entries = po.productentry_set.all()
    # s = 0
    # for q in entries.iterator():
    #     s += (q.rate * q.Qty) - (((q.Discount)/100) * (q.Qty * q.rate)) + q.Tax

    context = {'po':po,}
    # context = {'po':po,'entries':entries,'sum': s}
    return render(request,'finance/poinfo.html',context)


def createPO(request):
    po_form = PoForm()
    service_form=ServiceForm()
    # ent_form = PEntryForm()

   
    # ent_form = SEntryForm()
    if request.method == 'POST':
        inv_form = PoForm(request.POST)
        service_form=ServiceForm(request.POST)
        
        if inv_form.is_valid():
            inv_form.save()
            # pre_save.send(sender=Invoice)
            return redirect('poS')

        if service_form.is_valid():
            service_form.save()
            return redirect('create_po')
    # if request.method == 'POST':
    #     po_form = PoForm(request.POST)
    #     service_form=ServiceForm(request.POST)
    #     # ent_form = PEntryForm(request.POST)
    #     if service_form.is_valid():
    #         service_form.save()
    #         return redirect('create_po')

    #     if po_form.is_valid():
    #     # if po_form.is_valid() and ent_form.is_valid():
    #         po = po_form.save()
            # ent = ent_form.save(False)

            # ent.PO = po
            # ent.save()
            # return redirect('poS')

    # context = {'po_form':po_form,'ent_form':ent_form}
    context = {'po_form':po_form,'service_form':service_form}

    return render(request,'finance/po_form.html',context)


def updatePO(request,pk): # only for updating the invoice, for service entry create another view 
    po = PurchaseOrder.objects.get(id=pk)
    po_form = PoForm(instance=po)
    if request.method == 'POST':
        po_form = PoForm(request.POST,instance=po)
        if po_form.is_valid(): 
            po = po_form.save()
            
            return redirect('poS')
    context = {'po_form':po_form} 
    
    return render(request,'finance/updpo_form.html',context)


def updatePEnt(request,pk):  # PRODUCT ENTRY
    entry = ProductEntry.objects.get(id=pk)
    ent_form = PEntryForm(instance=entry)
    if request.method == 'POST':
        ent_form = PEntryForm(request.POST,instance=entry)
        ent = ent_form.save()

        return redirect('po')

    context = {'ent_form':ent_form} #,'ent_form':ent_form
    
    return render(request,'finance/updpoent_form.html',context)


def deletePO(request,pk):
    item = PurchaseOrder.objects.get(id=pk)
    if request.method == 'POST':
        item = PurchaseOrder.objects.get(id=pk)
        item.delete()
        return redirect('poS')

    context = {'item':item}
    return render(request,'finance/deletepo.html',context)

def deletePEnt(request,pk):
    item = ProductEntry.objects.get(id=pk)
    # obj = Invoice.objects.get(id=pk)
    if request.method == 'POST':
        item = ProductEntry.objects.get(id=pk)
        item.delete()
        # obj = Invoice.objects.get(id=pk)
        return redirect('po')

    context = {'item':item}
    return render(request,'finance/deletepo.html',context)
