from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authentication import TokenAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from products.api.serializers import ProductSerializer
from products.models import Product

class ObjectModelViewSetActionBasicMixin:

    @action(detail=True)
    def deactivate(self, request, **kwargs):
        """
            Change active data at False
            Example: http://127.0.0.1:8000/students/api/students/4/deactivate/
        """
        data = self.get_object()
        data.active = False
        data.save()

        serializer = self.serializer_class(data)
        return Response(serializer.data)

    @action(detail=True)
    def activate(self, request, **kwargs):
        """
            Change active data at False
            Example: http://127.0.0.1:8000/students/api/students/4/activate/
        """
        
        data = self.model.objects.get(id=self.kwargs.get('pk'))
        data.active = True
        data.save()

        serializer = self.serializer_class(data)
        return Response(serializer.data)

    @action(detail=False)
    def deactivate_all(self, request, **kwargs):
        """
            Change active data at False
            Example: http://127.0.0.1:8000/students/api/students/deactivate_all/
        """
        data = self.get_queryset()
        data.update(active=False)

        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def activate_all(self, request, **kwargs):
        """
            Change active data at True
            Example: http://127.0.0.1:8000/students/api/students/activate_all/
        """
        data = self.model.objects.all()
        data.update(active=True)

        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        data = self.get_object()
        data.active = False
        data.save()

        return Response('Object removed', status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['POST'])
    def change_status(self, request, **kwargs):
        """
            Change active data at True or False
            Example: http://127.0.0.1:8000/students/api/students/change_status/
        """
        status = True if request.data['active'] == 'True' else False

        data = self.get_queryset #Product.objects.all()
        data.update(active=status)

        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data)