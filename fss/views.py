from django.shortcuts import render, get_object_or_404
from unicodedata import category
from .models import Suggestion

def suggestion_list(request):
    suggestions = Suggestion.objects.select_related('category', 'status').all()

    # Фильтрация по категориям и статусам
    category = request.GET.get('category')
    status = request.GET.get('status')

    if category:
        suggestions = suggestions.filter(category__name=category)
    if status:
        suggestions = suggestions.filter(status__name=status)

    return render(request, 'fss/suggestion_list.html', {'suggestions': suggestions})

def suggestion_form(request):
    return render(request,'fss/suggestion_form.html',{})

def suggestion_detail(request, pk):
    suggestion = get_object_or_404(Suggestion, pk=pk)
    return render(request, 'fss/suggestion_detail.html', {'suggestion': suggestion})