from django.urls import path, include
from . import views

products_patterns = ([ 
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('categories/<int:pk>/<slug:slug>/', views.CategoryDetailView.as_view(), name='category'),
    path('categories/create/', views.CategoryCreate.as_view(), name='category-create'),
    path('categories/update/<int:pk>/', views.CategoryUpdate.as_view(), name='category-update'),
    path('categories/delete/<int:pk>/', views.CategoryDelete.as_view(), name='category-delete'), 
    
    path('', views.ProductListView.as_view(), name='products'),
    path('<int:pk>/<slug:slug>/', views.ProductDetailView.as_view(), name='product'),
    path('create/', views.ProductCreate.as_view(), name='create'),
    path('update/<int:pk>/', views.ProductUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', views.ProductDelete.as_view(), name='delete'),

    path('api/', include('products.api.urls')), 
], 'products')
