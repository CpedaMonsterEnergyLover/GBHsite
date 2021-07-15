from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('database.urls')),
    path('', views.welcome_site),
    path('signup', views.signup),
    path('signin', views.login_)
]
