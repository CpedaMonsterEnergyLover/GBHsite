from django.http import HttpResponse
from django.shortcuts import render


def wpage(request):
    return render(request, 'details/test.html')
