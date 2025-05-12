from django.shortcuts import render, get_object_or_404, redirect
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST

from .models import Category, Divisions, Suggestion, Status, Notification, Comment
from .forms import SuggestionForm, CommentForm
from django.contrib.auth.forms import UserCreationForm


@login_required
def home(request):
    unread_count = request.user.notifications.filter(is_read=False).count()
    return render(request, 'fss/home.html', {'unread_count': unread_count})


def password_reset(request):
    return render(request, 'registration/password_reset.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Пользователь {username} успешно зарегистрирован')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def suggestion_list(request):
    suggestions = Suggestion.objects.select_related('category', 'status').all()

    category = request.GET.get('category')
    status = request.GET.get('status')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if category:
        suggestions = suggestions.filter(category__name=category)
    if status:
        suggestions = suggestions.filter(status__name=status)
    if start_date:
        suggestions = suggestions.filter(date_create__gte=parse_date(start_date))
    if end_date:
        suggestions = suggestions.filter(date_create__lte=parse_date(end_date))

    paginator = Paginator(suggestions, 20)
    page = request.GET.get('page')

    try:
        suggestions = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        suggestions = paginator.page(1)

    return render(request, 'fss/suggestion_list.html', {'suggestions': suggestions})


@login_required
def suggestion_detail(request, suggestion_id):
    suggestion = get_object_or_404(Suggestion, id=suggestion_id)
    comments_list = suggestion.comments.order_by('-created_at')

    paginator = Paginator(comments_list, 4)
    page = request.GET.get('page')
    comments = paginator.get_page(page)

    form = CommentForm()

    return render(request, 'fss/suggestion_detail.html', {
        'suggestion': suggestion,
        'comments': comments,
        'form': form,
    })


@login_required
def add_comment(request, suggestion_id):
    suggestion = get_object_or_404(Suggestion, id=suggestion_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.suggestion = suggestion
            comment.user = request.user
            comment.save()
            return redirect('suggestion_detail', suggestion_id=suggestion.id)

    return redirect('suggestion_detail', suggestion_id=suggestion.id)


@login_required
def create_suggestion(request):
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.user = request.user
            suggestion.status = Status.objects.get(name='draft')
            suggestion.save()
            return redirect('my_suggestions')
    else:
        form = SuggestionForm()
    return render(request, 'fss/suggestion_form.html', {'form': form})


@login_required
def edit_suggestion(request, pk):
    suggestion = get_object_or_404(Suggestion, pk=pk, user=request.user)
    if suggestion.status.name != 'draft':
        return redirect('my_suggestions')

    if request.method == 'POST':
        form = SuggestionForm(request.POST, instance=suggestion)
        if form.is_valid():
            form.save()
            return redirect('my_suggestions')
    else:
        form = SuggestionForm(instance=suggestion)
    return render(request, 'fss/suggestion_form.html', {'form': form})


@login_required
def submit_suggestion(request, pk):
    suggestion = get_object_or_404(Suggestion, pk=pk, user=request.user)
    if suggestion.status.name == 'draft':
        suggestion.status = Status.objects.get(name='submitted')
        suggestion.save()
    return redirect('my_suggestions')


@login_required
def moderator_panel(request):
    suggestions = Suggestion.objects.select_related('user', 'status').order_by('-id')

    status_filter = request.GET.get('status')
    user_filter = request.GET.get('user')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if status_filter:
        suggestions = suggestions.filter(status__name=status_filter)
    if user_filter:
        suggestions = suggestions.filter(user__username__icontains=user_filter)
    if start_date:
        suggestions = suggestions.filter(date_create__gte=parse_date(start_date))
    if end_date:
        suggestions = suggestions.filter(date_create__lte=parse_date(end_date))

    paginator = Paginator(suggestions, 10)
    page = request.GET.get('page')
    suggestions_page = paginator.get_page(page)

    return render(request, 'fss/moderator_panel.html', {
        'suggestions': suggestions_page,
        'status_filter': status_filter,
        'user_filter': user_filter,
        'start_date': start_date,
        'end_date': end_date,
    })


@login_required
def my_suggestions(request):
    user_suggestions_list = Suggestion.objects.filter(user=request.user).order_by('-id')
    paginator = Paginator(user_suggestions_list, 5)
    page = request.GET.get('page')
    suggestions = paginator.get_page(page)
    return render(request, 'fss/my_suggestions.html', {'suggestions': suggestions})


@login_required
def reject_suggestion(request):
    if request.method == 'POST':
        suggestion_id = request.POST.get('suggestion_id')
        reason = request.POST.get('reason')
        action = request.POST.get('action')

        try:
            suggestion = Suggestion.objects.get(id=suggestion_id)
            status_obj = Status.objects.get(name=action)
            suggestion.status = status_obj
            suggestion.save()

            Comment.objects.create(
                suggestion=suggestion,
                user=request.user,
                text=reason
            )

            return JsonResponse({
                'success': True,
                'new_status': status_obj.get_name_display(),
                'status_class': get_status_class(status_obj.name),
            })
        except (Suggestion.DoesNotExist, Status.DoesNotExist):
            return JsonResponse({'success': False, 'error': 'Invalid data'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required
def approve_suggestion(request):
    if request.method == "POST":
        suggestion_id = request.POST.get("suggestion_id")
        status_name = request.POST.get("status")
        comment = request.POST.get("comment", "")

        # Проверяем наличие предложения
        suggestion = get_object_or_404(Suggestion, id=suggestion_id)

        # Проверяем наличие статуса
        try:
            status = Status.objects.get(name=status_name)
        except Status.DoesNotExist:
            return JsonResponse({"success": False, "error": "Статус не найден"}, status=400)

        # Обновляем статус предложения
        suggestion.status = status
        suggestion.save()

        # Добавляем комментарий, если он есть
        if comment:
            Comment.objects.create(
                suggestion=suggestion,
                user=request.user,
                text=comment
            )

        # Создаем уведомление для автора предложения
        Notification.objects.create(
            user=suggestion.user,
            message=f"Статус вашего предложения «{suggestion.title}» изменён на «{status.get_name_display()}»."
        )

        # Возвращаем успешный ответ с данными
        return JsonResponse({
            "success": True,
            "new_status": status.get_name_display(),
            "status_class": get_status_class(status.name),  # Если у тебя есть эта функция, возвращающая CSS-классы
        })

    return JsonResponse({"success": False, "error": "Метод не разрешен"}, status=405)


@login_required
def notifications_view(request):
    # Если использовал related_name="notifications" в модели Notification
    notifications = request.user.notifications.order_by('-created_at')

    # Если использовал notification_set (без указания related_name)
    # notifications = request.user.notification_set.order_by('-created_at')

    context = {
        'notifications': notifications
    }
    return render(request, 'fss/notifications.html', context)

@login_required
def unread_notification_count(request):
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'unread_count': count})

def get_status_class(status_name):
    status_classes = {
        'draft': 'bg-secondary',
        'submitted': 'bg-primary',
        'rejected': 'bg-danger',
        'archived': 'bg-dark',
        'approved': 'bg-success',
        'preparing': 'bg-info',
        'in_progress': 'bg-warning',
        'completed': 'bg-success',
    }
    return status_classes.get(status_name, 'bg-warning')
