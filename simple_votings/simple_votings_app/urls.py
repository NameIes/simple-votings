from django.urls import path
from .views import *
from django.contrib.auth import views as au_views

urlpatterns = [
    path('', index),
    path('create/', create_voting),
    path('voting/<int:voting_id>', voting),
    path('vote/<int:answer>', vote),
    path('like/<int:voting_id>', like),
    path('login/', au_views.LoginView.as_view()),
    path('logout/', au_views.LogoutView.as_view()),
    path('accounts/profile/', update_profile, name='profile'),
]
