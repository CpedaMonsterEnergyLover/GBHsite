from django.urls import path
from . import views

urlpatterns = [
    path('db/categories', views.categories),
    path('db', views.welcome_database),
    path('profile/hero', views.test)
]
