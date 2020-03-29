"""kmarket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from rest_framework.authtoken import views

from products.urls import products_patterns
from customers.urls import customers_patterns
from profiles.urls import profiles_patterns

urlpatterns = [
    path('', include('core.urls')),  
    path('products/', include(products_patterns)), 
    path('customers/', include(customers_patterns)),  

    path('admin/', admin.site.urls),
    path('api-token-auth/', views.obtain_auth_token), 
    ##path('api-auth/', include('rest_framework.urls)),

    # Paths of Auth
    path('accounts/', include('django.contrib.auth.urls')), 
    path('accounts/', include('registration.urls')), 

    # Paths de profiles
    path('profiles/', include(profiles_patterns)),
 
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns