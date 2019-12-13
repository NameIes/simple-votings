
from django.urls import path
from .views import *

urlpatterns = [
    path('', viewtest),
    path('bdex', bd_example),
]
