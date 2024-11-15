from django.shortcuts import render

def suggestion_list(request):
    return render(request,'fss/suggestion_list.html',{})

def suggestion_form(request):
    return render(request,'fss/suggestion_form.html',{})

