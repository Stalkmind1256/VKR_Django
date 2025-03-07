from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from .views import suggestion_detail, add_comment
from .views import user_suggestions


def redirect_home(request):
    return redirect('/home')


urlpatterns = [
    path('', redirect_home),
    path('home/', views.home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('list/', views.suggestion_list, name='suggestion_list'),
    # path('suggestions/', views.suggestion_create, name='suggestion_create'),
    path('suggestion/<int:suggestion_id>/', suggestion_detail, name='suggestion_detail'),
    path('suggest/', views.suggestion_form, name='suggestion_form'),
    path('register/', views.register, name='register'),

    # path('suggestion/<int:suggestion_id>/', views.suggestion_detail, name='suggestion_detail'),
    path('suggestion/<int:suggestion_id>/comment/', add_comment, name='add_comment'),

    path('my_suggestions/', user_suggestions, name='my_suggestions'),
    path('suggestion/<int:suggestion_id>/edit/', views.edit_suggestion, name='edit_suggestion'),
]