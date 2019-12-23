# -*- coding: utf-8 -*-
import datetime
from django.db import IntegrityError, transaction
# https://django.fun/docs/ru/3.0/topics/db/transactions/
from django.contrib import messages
# https://docs.djangoproject.com/en/3.0/ref/contrib/messages/

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect

from .models import modelTest, Vote, VotingAnswer, Voting
from .forms import AddVotingForm, UserForm, ProfileForm


def viewtest(request):
    context = {}

    quest = modelTest.objects.get(id=1)
    quest.click_count += 1
    quest.save()

    context['question'] = quest

    return render(request, 'base.html', context)


def vote(request, answer):
    if request.method == 'POST':
        answer = VotingAnswer.objects.get(id=int(answer))
        vote = Vote(answer=answer)
        vote.save()

    return HttpResponse('Ваш голос учтён!')


@login_required
def create_voting(request):
    context = {}
    context['form'] = AddVotingForm()
    context['votings'] = Voting.objects.all()

    if request.method == 'POST':
        form = AddVotingForm(request.POST)
        if form.is_valid():
            voting_item = Voting(text=form.data['question'])
            voting_item.save()

            count = int(request.POST.get('answers_count'))
            for i in range(1, count + 1):
                text = request.POST.get('answer' + str(i))
                item = VotingAnswer(text=text, voting=voting_item)
                item.save()

    return render(request, 'bd_example.html', context)


@login_required
def bd_example(request):
    context = {}
    context['flag'] = 'Appear'
    # context = {'form': AddVotingForm()}

    # if request.method == 'POST':
    #     form = AddVotingForm(request.POST)
    #     if form.is_valid():
    #         voting_item = Voting(text=form.data['question'],
    #                              start=datetime.datetime.now())
    #         voting_item.save()

    #         answers = form.data['answers'].split('\n')
    #         for i in answers:
    #             if len(i) <= 200:
    #                 answer_item = VotingAnswer(text=i, voting=voting_item)
    #                 answer_item.save()

    context['votings'] = Voting.objects.all()
    #lst = []
    #for voting in votings:
    #    lst.append((voting, VotingAnswer.objects.filter(voting=voting)))

    #if len(lst) > 0:
    #    context['data'] = lst

    return render(request, 'bd_example.html', context)


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, u'Ваш профиль был успешно обновлен!')
            return redirect('profile')
        else:
            messages.error(request, u'Пожалуйста, исправьте ошибки.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
