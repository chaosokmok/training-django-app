from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.training_list, name='training_list'),
    path('add/', views.training_create, name='training_create'),
    path('dashboard/', views.training_dashboard, name='training_dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='trainings/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('trainings/pdf-preview/', views.preview_pdf, name='preview_pdf'),
    path('trainings/<int:pk>/', views.training_delete, name='training_delete'),
    path('training/delete/<int:pk>/', views.training_delete, name='training_delete'),
    
]
