from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from .views import suggestion_detail, add_comment, import_users, edit_user, rate_suggestion
from .views import suggestions_stats_api
from .views import stats
from .views import user_management ,delete_user

def redirect_home(request):
    return redirect('/home')


urlpatterns = [
    path('', redirect_home),
    path('home/', views.home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('list/', views.suggestion_list, name='suggestion_list'),
    path('suggestion/<int:suggestion_id>/', suggestion_detail, name='suggestion_detail'),
    path('register/', views.register, name='register'),

    path('suggestion/<int:suggestion_id>/comment/', add_comment, name='add_comment'),
    path('my_suggestions/', views.my_suggestions, name='my_suggestions'),


    path('suggestions/<int:pk>/edit/', views.edit_suggestion, name='edit_suggestion'),

    path('suggestions/create/', views.create_suggestion, name='create_suggestion'),
    path('suggestions/<int:pk>/submit/', views.submit_suggestion, name='submit_suggestion'),
    path('reject-suggestion/', views.reject_suggestion, name='reject_suggestion'),
    path('approve-suggestion/', views.approve_suggestion, name='approve_suggestion'),
    path('moderator/', views.moderator_panel, name='moderator_panel'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('ajax/unread-count/', views.unread_notification_count, name='unread_notification_count'),
    path('api/stats/', suggestions_stats_api, name='suggestions_stats_api'),
    path('stats/', stats, name='stats'),
    path('export/csv/', views.export_suggestions_csv, name='export_suggestions_csv'),
    path('export/excel/', views.export_suggestions_excel, name='export_suggestions_excel'),
    path('import-users/', import_users, name='import_users'),

    path('users/', user_management, name='user_management'),
    path('users/<int:user_id>/delete/', delete_user, name='delete_user'),
    path('users/<int:user_id>/edit/', edit_user, name='edit_user'),
    path('notifications/mark_read/', views.mark_notifications_read, name='mark_notifications_read'),
    path('rate-suggestion/', rate_suggestion, name='rate_suggestion'),

   # path('notifications/clear/', views.clear_notifications, name='clear_notifications'),
]
