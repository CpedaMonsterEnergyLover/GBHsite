from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from .forms import SignUpForm
from django.shortcuts import redirect


def welcome_site(request):
    return render(request, 'sitepages/home/main.html')


def signup(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            # gets form fields
            password = signup_form.cleaned_data['password']
            username = signup_form.cleaned_data['username']
            email = signup_form.cleaned_data['email']
            birthday = signup_form.cleaned_data['birthday']
            # creates a new user
            user = User.objects.create_user(username, email, password)
            user.profile.birth_date = birthday
            user.save()
            # render submit page
            return render(request, "sitepages/signup/submit/main.html", {'username': username, 'email': email})
        else:
            return render(request, 'sitepages/signup/main.html', {'signup_form': signup_form})
    else:
        signup_form = SignUpForm()

    return render(request, 'sitepages/signup/main.html', {'signup_form': signup_form})


def settings(request):
    return render(request, 'sitepages/profile/settings/main.html')


@login_required
def profile(request):
    return render(request, 'sitepages/profile/main.html')


@login_required
def logout_user(request):
    logout(request)
    return redirect('/')
