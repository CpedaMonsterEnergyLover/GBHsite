from django.shortcuts import render


def categories(request):
    return render(request, 'dbpages/categories/root.html')


def welcomedatabase(request):
    return render(request, 'dbpages/home/root.html')

