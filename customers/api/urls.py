from django.urls import path, include
from django.conf import settings

from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('customers', views.CustomerViewSet, base_name="api-customers")

urlpatterns = [
    path( '', include(router.urls) ),
]