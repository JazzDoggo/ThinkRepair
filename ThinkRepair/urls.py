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

from thinkpart import views as thinkpart_views
from thinkuser import views as thinkuser_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('user/register/', thinkpart_views.UserRegisterView.as_view(), name='user_register'),
    path('user/login/', thinkpart_views.UserLoginView.as_view(), name='user_login'),
    path('user/logout/', thinkpart_views.UserLogoutView.as_view(), name='user_logout'),
    path('user/edit/', thinkpart_views.UserUpdateView.as_view(), name='user_update'),

    path('', thinkpart_views.HomeView.as_view(), name='home'),
    path('parts/', thinkpart_views.PartListView.as_view(), name='part_list'),
    path('parts/add/', thinkpart_views.PartAddView.as_view(), name='part_add'),
    path('parts/<int:pk>/', thinkpart_views.PartDetailView.as_view(), name='part_detail'),
    path('parts/<int:pk>/edit/', thinkpart_views.PartUpdateView.as_view(), name='part_update'),
    path('parts/<int:pk>/delete/', thinkpart_views.PartDeleteView.as_view(), name='part_delete'),
    path('parts/search/', thinkpart_views.PartSearchView.as_view(), name='part_search'),

    path('laptops/', thinkpart_views.LaptopListView.as_view(), name='laptop_list'),
    path('laptops/add/', thinkpart_views.LaptopAddView.as_view(), name='laptop_add'),
    path('laptops/<int:pk>/', thinkpart_views.LaptopDetailView.as_view(), name='laptop_detail'),
    path('laptops/<int:pk>/edit/', thinkpart_views.LaptopUpdateView.as_view(), name='laptop_update'),
    path('laptops/<int:pk>/delete/', thinkpart_views.LaptopDeleteView.as_view(), name='laptop_delete'),

    path('parts/<int:part_pk>/laptop/add/', thinkpart_views.PartLaptopAddView.as_view(), name='part_laptop_add'),
    path('laptops/<int:laptop_pk>/parts/add/', thinkpart_views.LaptopPartAddView.as_view(), name='laptop_part_add'),
    path('laptops/<int:laptop_pk>/parts/<int:laptop_part_pk>/', thinkpart_views.LaptopPartUpdateView.as_view(),
         name='laptop_part_update'),
    path('laptops/<int:laptop_pk>/parts/<int:laptop_part_pk>/delete/', thinkpart_views.LaptopPartDeleteView.as_view(),
         name='laptop_part_delete'),

    path('user/laptops/add/', thinkuser_views.UserLaptopAddView.as_view(), name='user_laptop_add'),
    path('user/laptops/', thinkuser_views.UserLaptopListView.as_view(), name='user_laptop_list'),
    path('user/laptops/<int:pk>/current/', thinkuser_views.UserLaptopDetailCurrentView.as_view(),
         name='user_laptop_current'),
    path('user/laptops/<int:pk>/history/', thinkuser_views.UserLaptopDetailHistoryView.as_view(),
         name='user_laptop_history'),
    path('user/laptops/<int:pk>/delete/', thinkuser_views.UserLaptopDeleteView.as_view(), name='user_laptop_delete'),
    path('user/laptops/<int:user_laptop_pk>/replace/<int:laptop_part_pk>/',
         thinkuser_views.UserReplacedPartAddView.as_view(),
         name='user_laptop_replace_part'),
]
