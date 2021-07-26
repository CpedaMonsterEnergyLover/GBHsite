from django.urls import path
from . import views

urlpatterns = [
    path('db/categories', views.categories),
    path('db', views.welcome_database),
    path('profile/<str:user_name>/hero/<int:hero_set_id>', views.inspect_hero),
    path('group/create', views.create_group)
]
