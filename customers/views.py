from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from .models import Customer
from .forms import CustomerForm
from sales.models import Sale 
# Create your views here.

class CustomerListView(ListView):
    model = Customer
    paginate_by = 25

class CustomerDetailView(DetailView):
    model = Customer

class CustomerSalesDetailView(DetailView):
    """Returns all sales of a particular customer"""
    model = Customer
    template_name = 'customers/customer_sales_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['sales'] = Sale.objects.filter( client_id=self.object.id )

        return ctx

@method_decorator(staff_member_required, name='dispatch')
class CustomerDelete(DeleteView):
    model = Customer

    def get_success_url(self):
        return reverse_lazy('customers:customers', args=[self.object.id]) + "?remove"

@method_decorator(staff_member_required, name='dispatch')
class CustomerCreate(CreateView):
    model = Customer
    form_class = CustomerForm
    
    def get_success_url(self):
        return reverse_lazy('customers:customers', args=[self.object.id]) + "?add"


@method_decorator(staff_member_required, name='dispatch')
class CustomerUpdate(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse_lazy('customers:update', args=[self.object.id]) + "?ok"