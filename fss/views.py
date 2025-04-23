from django.shortcuts import render, get_object_or_404,redirect
from django.utils.dateparse import parse_date
from django.utils.text import re_prt

from .models import Category, Divisions, Suggestion, Status
from .models import Suggestion, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CommentForm
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .forms import SuggestionForm
from django.core.exceptions import PermissionDenied

# @login_required
# def add_comment(request, suggestion_id):
#     suggestion = get_object_or_404(Suggestion, id=suggestion_id)
#
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.suggestion = suggestion
#             comment.author = request.user
#             comment.save()
#             return redirect('suggestion_detail', suggestion_id=suggestion.id)
#     else:
#         form = CommentForm()
#
#     return render(request, 'fss/add_comment.html', {'form': form, 'suggestion': suggestion})

def suggestion_list(request):
    suggestions = Suggestion.objects.select_related('category', 'status').all()

    # Фильтрация по категориям и статусам
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

    paginator = Paginator(suggestions, 20)  # По 20 элементов на страницу
    page = request.GET.get('page')

    try:
        suggestions = paginator.page(page)
    except PageNotAnInteger:
        suggestions = paginator.page(1)
    except EmptyPage:
        suggestions = paginator.page(paginator.num_pages)

    return render(request, 'fss/suggestion_list.html', {'suggestions': suggestions})

def suggestion_form(request):
    categories = Category.objects.all()
    divisions = Divisions.objects.all()
    return render(request,'fss/suggestion_form.html',{'categories': categories, 'divisions':divisions})


from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Suggestion, Comment
from .forms import CommentForm


def suggestion_detail(request, suggestion_id):
    suggestion = get_object_or_404(Suggestion, id=suggestion_id)
    comments_list = Comment.objects.filter(suggestion=suggestion).order_by('-created_at')

    # Пагинация: 5 комментариев на страницу
    paginator = Paginator(comments_list, 4)
    page_number = request.GET.get('page')
    comments = paginator.get_page(page_number)

    form = CommentForm()

    return render(request, 'fss/suggestion_detail.html', {
        'suggestion': suggestion,
        'comments': comments,  # Передаём объект Paginator
        'form': form
    })

def home(request):
    return render(request, 'fss/home.html')

def password_reset(request):
    return render(request, 'registration/password_reset.html')
# def suggestion_create(request):
#     categories = Category.objects.all()
#     return render(request,'api_v0/suggestion_create.html',{'categories': categories})

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
            return redirect('suggestion_detail', suggestion_id=suggestion.id)  # 🛠 Исправлено!

    else:
        form = CommentForm()

    return render(request, 'fss/suggestion_detail.html', {
        'suggestion': suggestion,
        'comments': suggestion.comments.all(),
        'form': form,
    })

@login_required
def user_suggestions(request):
    suggestions = Suggestion.objects.filter(user=request.user)
    return render(request, 'fss/my_suggestions.html', {'suggestions': suggestions})

def my_suggestions(request):
    user_suggestions = Suggestion.objects.filter(user=request.user)
    return render(request, 'fss/my_suggestions.html', {'suggestions': user_suggestions})

@login_required
def edit_suggestion(request, suggestion_id):
    suggestion = get_object_or_404(Suggestion, id=suggestion_id)


    # if suggestion.author != request.user:
    #     raise PermissionDenied("Вы не можете редактировать это предложение.")

    if request.method == 'POST':
        form = SuggestionForm(request.POST, instance=suggestion)
        if form.is_valid():
            form.save()
            return redirect('fss/my_suggestions', suggestion_id=suggestion.id)
    else:
        form = SuggestionForm(instance=suggestion)

    return render(request, 'fss/edit_suggestion.html', {'form': form, 'suggestion': suggestion})

def create_suggestion(request):
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.user = request.user  # Привязываем к текущему пользователю
            suggestion.status = Status.objects.get(name='draft')  # Статус "Черновик"
            suggestion.save()
            return redirect('my_suggestions')
    else:
        form = SuggestionForm()
    return render(request, 'fss/suggestion_form.html', {'form': form})


def edit_suggestion(request, pk):
    suggestion = get_object_or_404(Suggestion, pk=pk, user=request.user)
    if suggestion.status.name != 'draft':
        return redirect('fss/my_suggestions')  # Запрещаем редактирование, если это не черновик

    if request.method == 'POST':
        form = SuggestionForm(request.POST, instance=suggestion)
        if form.is_valid():
            form.save()
            return redirect('my_suggestions')
    else:
        form = SuggestionForm(instance=suggestion)
    return render(request, 'fss/suggestion_form.html', {'form': form})


def submit_suggestion(request, pk):
    suggestion = get_object_or_404(Suggestion, pk=pk, user=request.user)
    if suggestion.status.name == 'draft':
        suggestion.status = Status.objects.get(name='submitted')  # Меняем статус на "В ожидании"
        suggestion.save()
    return redirect('my_suggestions')

def get_status_class(status_name):
    """Возвращает класс для отображения статуса"""
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


def reject_suggestion(request):
    if request.method == "POST":
        suggestion_id = request.POST.get("suggestion_id")
        reason = request.POST.get("reason")
        action = request.POST.get("action")

        suggestion = get_object_or_404(Suggestion, id=suggestion_id)

        # Получаем статус "archived" или "draft" из модели Status
        if action == "archive":
            status = get_object_or_404(Status, name="archived")
        elif action == "draft":
            status = get_object_or_404(Status, name="draft")
        else:
            return JsonResponse({"success": False, "error": "Invalid action"})

        # Устанавливаем новый статус и комментарий
        suggestion.status = status
        suggestion.moderator_comment = reason
        suggestion.save()

        return JsonResponse({"success": True})

    return JsonResponse({"success": False})


@login_required
def approve_suggestion(request):
    if request.method == "POST":
        suggestion_id = request.POST.get("suggestion_id")
        status_name = request.POST.get("status")
        comment = request.POST.get("comment", "")

        # Получаем объекты Suggestion и Status или возвращаем 404
        suggestion = get_object_or_404(Suggestion, id=suggestion_id)
        status = get_object_or_404(Status, name=status_name)

        # Обновляем статус и комментарий модератора
        suggestion.status = status
        suggestion.moderator_comment = comment
        suggestion.moderator = request.user
        suggestion.save()

        return JsonResponse({
            "success": True,
            "new_status": status.get_name_display(),
            "status_class": get_status_class(status.name)
        })

    return JsonResponse({"success": False, "error": "Метод не разрешен"}, status=405)