from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from .views import suggestion_detail, add_comment



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

    path('my_suggestions/', views.my_suggestions, name='my_suggestions'),
    path('suggestion/<int:suggestion_id>/edit/', views.edit_suggestion, name='edit_suggestion'),

    path('suggestions/create/', views.create_suggestion, name='create_suggestion'),
    path('suggestions/<int:pk>/edit/', views.edit_suggestion, name='edit_suggestion'),
    path('suggestions/<int:pk>/submit/', views.submit_suggestion, name='submit_suggestion'),
    path('reject-suggestion/', views.reject_suggestion, name='reject_suggestion'),
<<<<<<< HEAD
]
re_prt
=======
    path('profile/', views.profile_view, name='profile'),
]
>>>>>>> 039b8bdaacc5471461e917d685426f586a5bf57b
