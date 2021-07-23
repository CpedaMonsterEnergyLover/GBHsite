from django.shortcuts import render


def categories(request):
    return render(request, 'dbpages/categories/root.html')


def welcome_database(request):
    return render(request, 'dbpages/home/root.html')


def test(request):
    return render(request, 'profiles_pages/explore_hero/hero.html')

