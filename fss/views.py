from django.shortcuts import render, get_object_or_404
from django.utils.dateparse import parse_date
from .models import Category
from .models import Suggestion


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

    return render(request, 'fss/suggestion_list.html', {'suggestions': suggestions})

def suggestion_form(request):
    categories = Category.objects.all()
    return render(request,'fss/suggestion_form.html',{'categories': categories})

def suggestion_detail(request, pk):
    suggestion = get_object_or_404(Suggestion, pk=pk)
    return render(request, 'fss/suggestion_detail.html', {'suggestion': suggestion})

def home(request):
    return render(request, 'fss/home.html')

def password_reset(request):
    return render(request, 'registration/password_reset.html')
# def suggestion_create(request):
#     categories = Category.objects.all()
#     return render(request,'api_v0/suggestion_create.html',{'categories': categories})

