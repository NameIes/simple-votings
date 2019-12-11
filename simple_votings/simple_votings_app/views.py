from django.shortcuts import render
from .models import modelTest
# Create your views here.

def viewtest(request):
    context = {}

    quest = modelTest.objects.get(id=1)
    quest.click_count += 1
    quest.save()

    context['question'] = quest

    return render(request,'base.html', context)