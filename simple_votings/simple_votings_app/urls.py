from django.urls import path
from .views import *

urlpatterns = [
    # path('', viewtest),
    path('', bd_example),
    path('create', create_voting),
    path('vote/<int:answer>', vote)
]
