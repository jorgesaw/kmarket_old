from django.urls import path, include
from django.conf import settings

from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, base_name="api-products")
router.register('categories', views.CategoryViewSet, base_name="api-categories")

urlpatterns = [
    path( '', include(router.urls) ),
]