from django.http import HttpResponse
from django.shortcuts import render


def categories(request):
    return render(request, 'pages/categories/main.html')
