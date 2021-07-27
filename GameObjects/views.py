from django.shortcuts import render


def categories(request):
    return render(request, 'db_pages/categories/root.html')


def welcome_database(request):
    return render(request, 'db_pages/home/root.html')
