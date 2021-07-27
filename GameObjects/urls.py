from django.urls import path

from GameObjects import views

urlpatterns = [
    path('db/categories', views.categories),
    path('db', views.welcome_database),
]
