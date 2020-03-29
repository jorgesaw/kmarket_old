from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import (
    AllowAny, 
    IsAuthenticatedOrReadOnly, 
    IsAdminUser,
    DjangoModelPermissions
)
from rest_framework.authentication import TokenAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from customers.models import Customer
from .serializers import CustomerSerializer
from utils.views_mixin import ObjectModelViewSetActionBasicMixin

class CustomerViewSet(ObjectModelViewSetActionBasicMixin, viewsets.ModelViewSet):
    model = Customer
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ('last_name',)
    search_fields = ('last_name', )
    ordering_fields = ('id', 'last_name',)
    ordering = ('last_name', 'first_name') # Ordenamiento por defecto al mostrar una consulta de datos
    #lookup_field = 'last_name'
    authentication_classes = [TokenAuthentication,]
    permission_classes = [DjangoModelPermissions,]
    
    def get_queryset(self):
        #import pdb;pdb.set_trace()
        #http://127.0.0.1:8000/students/api/students/?id=2&active=True
        #http://127.0.0.1:8000/students/api/students/?last_name=eo
        #http://127.0.0.1:8000/students/api/students/?search=eo
        #http://127.0.0.1:8000/students/api/students/?ordering=name
        #http://127.0.0.1:8000/students/api/students/?ordering=-name
        id = self.request.query_params.get('id', None)
        status = False if self.request.query_params.get('active') == 'False' else True
        last_name = self.request.query_params.get('last_name', None)

        if id:
            data = Customer.objects.filter(id=id, active=status)
        elif last_name:
            data = Customer.objects.filter(last_name__icontains=last_name, active=status)
        else:
            data = Customer.objects.filter(active=True)
        return data
