from django.shortcuts import render, get_object_or_404,redirect
from django.utils.dateparse import parse_date
from .models import Category, Divisions
from .models import Suggestion
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

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

def suggestion_detail(request, pk):
    suggestion = get_object_or_404(Suggestion, pk=pk)
    comments = suggestion.comments.all()
    form = CommentForm()  # Добавляем форму комментариев

    return render(request, 'fss/suggestion_detail.html', {
        'suggestion': suggestion,
        'comments': comments,
        'form': form,  # Передаем форму в шаблон
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

    # Если POST-запрос, обрабатываем форму
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.suggestion = suggestion
            comment.user = request.user
            comment.save()
            return redirect('suggestion_detail', pk=suggestion.id)
    else:
        form = CommentForm()

    # Передаем форму в шаблон
    return render(request, 'fss/suggestion_detail.html', {
        'suggestion': suggestion,
        'comments': suggestion.comments.all(),
        'form': form,  # Передаем форму в шаблон
    })