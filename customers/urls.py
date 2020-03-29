from django.urls import path, include
from . import views

customers_patterns = ([ 
    path('', views.CustomerListView.as_view(), name='customers'),
    path('<int:pk>/<slug:slug>/', views.CustomerDetailView.as_view(), name='customer'),
    path('create/', views.CustomerCreate.as_view(), name='create'),
    path('update/<int:pk>/', views.CustomerUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', views.CustomerDelete.as_view(), name='delete'), 
    
    path('customer_sales/<int:pk>/<slug:slug>/', views.CustomerSalesDetailView.as_view(), name='customer_sales'), 

    path('api/', include('customers.api.urls')), 
], 'customers')
