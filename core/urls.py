from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name="home"),
    path('sample/', views.SamplePageView.as_view(), name="sample"),
]