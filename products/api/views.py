from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authentication import TokenAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from products.models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from utils.views_mixin import ObjectModelViewSetActionBasicMixin

class CategoryViewSet(ObjectModelViewSetActionBasicMixin, viewsets.ModelViewSet):
    model = Category
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ('name',)
    search_fields = ('name', )
    ordering_fields = ('id', 'name',)
    ordering = ('name', ) # Ordenamiento por defecto al mostrar una consulta de datos
    #lookup_field = 'name'
    authentication_classes = [TokenAuthentication,]
    
    def get_queryset(self):
        #import pdb;pdb.set_trace()
        #http://127.0.0.1:8000/students/api/students/?id=2&active=True
        #http://127.0.0.1:8000/students/api/students/?name=eo
        #http://127.0.0.1:8000/students/api/students/?search=eo
        #http://127.0.0.1:8000/students/api/students/?ordering=name
        #http://127.0.0.1:8000/students/api/students/?ordering=-name
        id = self.request.query_params.get('id', None)
        status = False if self.request.query_params.get('active') == 'False' else True
        name = self.request.query_params.get('name', None)

        if id:
            data = Category.objects.filter(id=id, active=status)
        elif name:
            data = Category.objects.filter(name__icontains=name, active=status)
        else:
            data = Category.objects.filter(active=True)
        return data


class ProductViewSet(ObjectModelViewSetActionBasicMixin, viewsets.ModelViewSet):
    model = Product
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ('name',)
    search_fields = ('name', )
    ordering_fields = ('id', 'name',)
    ordering = ('name', ) # Ordenamiento por defecto al mostrar una consulta de datos
    #lookup_field = 'name'
    authentication_classes = [TokenAuthentication,]
    
    def get_queryset(self):
        #import pdb;pdb.set_trace()
        #http://127.0.0.1:8000/students/api/students/?id=2&active=True
        #http://127.0.0.1:8000/students/api/students/?name=eo
        #http://127.0.0.1:8000/students/api/students/?search=eo
        #http://127.0.0.1:8000/students/api/students/?ordering=name
        #http://127.0.0.1:8000/students/api/students/?ordering=-name
        id = self.request.query_params.get('id', None)
        status = False if self.request.query_params.get('active') == 'False' else True
        name = self.request.query_params.get('name', None)

        if id:
            data = Product.objects.filter(id=id, active=status)
        elif name:
            data = Product.objects.filter(name__icontains=name, active=status)
        else:
            data = Product.objects.filter(active=True)
        return data
