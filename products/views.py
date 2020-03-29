from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin

from .models import Product, Category, ProductWithoutPrice
from .forms import ProductForm, CategoryForm, ProductWithoutPriceForm
from core.views import StaffRequiredMixin
# Create your views here.

class CategoryListView(ListView):
    model = Category
    paginate_by = 25

class CategoryDetailView(DetailView):
    model = Category

@method_decorator(staff_member_required(login_url=settings.LOGIN_URL), name='dispatch')
class CategoryCreate(SuccessMessageMixin, CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('products:categories')
    success_message = "Datos creados exitosamente."

@method_decorator(staff_member_required(login_url=settings.LOGIN_URL), name='dispatch')
class CategoryUpdate(SuccessMessageMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name_suffix = "_update_form"
    success_message = "Datos actualizados exitosamente."

    def get_success_url(self):
        return reverse_lazy('products:category-update', args=[self.object.id]) + "?ok"

@method_decorator(staff_member_required(login_url=settings.LOGIN_URL), name='dispatch')
class CategoryDelete(SuccessMessageMixin, DeleteView):
    model = Category
    #success_url = reverse_lazy('products:categories')
    success_message = "Datos eliminados exitosamente."

    def get_success_url(self):
        return reverse_lazy('products:categories') + "?remove"

class ProductListView(ListView):
    model = Product
    paginate_by = 25

class ProductDetailView(DetailView):
    model = Product

@method_decorator(staff_member_required(login_url=settings.LOGIN_URL), name='dispatch')
class ProductCreate(SuccessMessageMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('products:products')

@method_decorator(staff_member_required(login_url=settings.LOGIN_URL), name='dispatch')
class ProductUpdate(SuccessMessageMixin, UpdateView):
    model = Product
    form_class = Product
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse_lazy('products:update', args=[self.object.id]) + "?ok"

@method_decorator(staff_member_required(login_url=settings.LOGIN_URL), name='dispatch')
class ProductDelete(SuccessMessageMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('products:products')
