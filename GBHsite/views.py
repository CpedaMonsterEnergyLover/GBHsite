from django.shortcuts import render


def welcomesite(request):
    return render(request, 'sitepages/home/root.html')


def signup(request):
    return render(request, 'sitepages/signup/root.html')
