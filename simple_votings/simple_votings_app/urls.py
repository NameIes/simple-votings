from django.urls import path
from .views import *
from django.contrib.auth import views as au_views

urlpatterns = [
    # path('', viewtest),
    path('', bd_example),
    path('create', create_voting),
    path('vote/<int:answer>', vote),
    path('login/', au_views.LoginView.as_view()),
    path('logout/', au_views.LogoutView.as_view()),
]
