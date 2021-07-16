from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('database.urls')),
    path('', views.welcome_site),
    path('signup', views.signup),
    path('login', auth_views.LoginView.as_view(template_name='sitepages/login/main.html',
                                               authentication_form=UserLoginForm,
                                               redirect_field_name='/db')),
    path('profile', views.profile),
    path('profile/settings', views.settings),
    path('profile/logout', views.logout_user)
]
