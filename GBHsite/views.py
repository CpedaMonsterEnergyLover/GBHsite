from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render
from .forms import SignUpForm, LoginForm
from django.shortcuts import redirect


def welcome_site(request):
    return render(request, 'sitepages/home/root.html')


def signup(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            password = signup_form.cleaned_data['password']
            username = signup_form.cleaned_data['username']
            email = signup_form.cleaned_data['email']
            birthday = signup_form.cleaned_data['birthday']
            user = User.objects.create_user(username, email, password)
            user.profile.birth_date = birthday
            user.save()
            return render(request, "sitepages/signup/submit/root.html", {'username': username, 'email': email})
        else:
            if signup_form.has_error('email'):
                signup_form.add_error(None, 'Enter a valid email address')
            return render(request, 'sitepages/signup/root.html', {'signup_form': signup_form})
    else:
        signup_form = SignUpForm()

    return render(request, 'sitepages/signup/root.html', {'signup_form': signup_form})


def login_(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login_password = login_form.cleaned_data['password']
            login_username = login_form.cleaned_data['username']
            user = authenticate(username=login_username, password=login_password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    response = redirect('/')
                else:
                    print("disabled account")
                    return render(request, 'sitepages/login/root.html', {'login_form': login_form})
                    # Return a 'disabled account' error message
            else:
                print("invalid login")
                return render(request, 'sitepages/login/root.html', {'login_form': login_form})
                # Return an 'invalid login' error message.
        else:
            print(login_form.errors)
    else:
        login_form = LoginForm()

    return render(request, 'sitepages/login/root.html', {'login_form': login_form})


