"""
URL configuration for ThinkRepair project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path

from thinkpart import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),

    path('', views.HomeView.as_view(), name='home'),
    path('parts/', views.PartListView.as_view(), name='part_list'),
    path('parts/add/', views.PartAddView.as_view(), name='part_add'),
    path('parts/<int:pk>/', views.PartDetailView.as_view(), name='part_detail'),
    path('parts/edit/<int:pk>/', views.PartUpdateView.as_view(), name='part_update'),
    path('parts/delete/<int:pk>/', views.PartDeleteView.as_view(), name='part_delete'),

    path('laptops/', views.LaptopListView.as_view(), name='laptop_list'),
    path('laptops/add/', views.LaptopAddView.as_view(), name='laptop_add'),
    path('laptops/<int:pk>/', views.LaptopDetailView.as_view(), name='laptop_detail'),
    path('laptops/edit/<int:pk>/', views.LaptopUpdateView.as_view(), name='laptop_update'),
    path('laptops/delete/<int:pk>/', views.LaptopDeleteView.as_view(), name='laptop_delete'),

    path('laptops/<int:laptop_pk>/parts/add/', views.LaptopPartAddView.as_view(), name='laptop_part_add'),
    path('laptops/<int:laptop_pk>/parts/<int:laptop_part_pk>/', views.LaptopPartUpdateView.as_view(),
         name='laptop_part_update'),
]
