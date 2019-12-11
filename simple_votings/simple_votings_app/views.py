from django.shortcuts import render

# Create your views here.

def viewtest(request):
    return render(request,'base.html',{})