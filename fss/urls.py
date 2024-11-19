from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

def redirect_home(request):
    return redirect('/home')

urlpatterns = [
    path('', redirect_home),
    path('home', views.home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('', views.suggestion_list, name='suggestion_list'),
    # path('suggestions/', views.suggestion_create, name='suggestion_create'),
    path('suggestion/<int:pk>/', views.suggestion_detail, name='suggestion_detail'),
    path('suggest/', views.suggestion_form, name='suggestion_form'),
]