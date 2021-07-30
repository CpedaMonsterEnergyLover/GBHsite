from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView
from .schema import schema

from . import views
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Profiles.urls')),
    path('', include('GameObjects.urls')),
    path('', views.welcome_site),
    path('signup', views.signup),
    path('login', auth_views.LoginView.as_view(template_name='site_pages/login/main.html',
                                               authentication_form=UserLoginForm,
                                               redirect_field_name='/profile')),
    path('logout', views.logout_user),
    path("graphql", GraphQLView.as_view(graphiql=True, schema=schema)),
]

