from django.urls import path
from . import views

urlpatterns = [
    path('', views.suggestion_list, name='suggestion_list'),
    path('suggestions/', views.suggestion_form, name='suggestion_form'),
    path('suggestion/<int:pk>/', views.suggestion_detail, name='suggestion_detail'),
]