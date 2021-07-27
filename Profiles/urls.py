from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:name>', views.profile),
    path('settings', views.settings),
    path('settings/redirect-success/<str:action>/', views.redirect_success),
    path('profile/<str:user_name>/hero/<int:hero_set_id>', views.inspect_hero),
    path('group/create', views.create_group)
]
