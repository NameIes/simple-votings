from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import VotingAnswer, Voting, Vote, Like, Comment
from .forms import AddVotingForm, AddCommentForm
# -*- coding: utf-8 -*-
import datetime
from django.db import IntegrityError, transaction
# https://django.fun/docs/ru/3.0/topics/db/transactions/
from django.contrib import messages
# https://docs.djangoproject.com/en/3.0/ref/contrib/messages/

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect

from .models import Vote, VotingAnswer, Voting
from .forms import AddVotingForm, UserForm, ProfileForm


@login_required
def voting(request, voting_id):
    context = {}
    context['voting'] = Voting.objects.get(id=voting_id)
    context['form'] = AddCommentForm()

    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment_item = Comment(
                text=form.data['comment'],
                voting=Voting.objects.get(id=voting_id),
                user=request.user
            )
            comment_item.save()

    return render(request, 'voting.html', context)


@login_required
def vote(request, answer):
    if request.method == 'POST':
        answer_item = VotingAnswer.objects.get(id=answer)
        vote_item = Vote(
            answer=answer_item,
            user=request.user
        )
        vote_item.save()

    return redirect('/voting/' + str(VotingAnswer.objects.get(id=answer).voting.id))


@login_required
def like(request, voting_id):
    if request.method == 'POST':
        voting_item = Voting.objects.get(id=voting_id)
        like_item = Like(
            voting=voting_item,
            user=request.user
        )
        like_item.save()

    return redirect('/voting/' + str(voting_id))


@login_required
def create_voting(request):
    context = {}
    context['form'] = AddVotingForm()

    if request.method == 'POST':
        form = AddVotingForm(request.POST)
        if form.is_valid():
            voting_item = Voting(
                text=form.data['question'],
                user=request.user
            )
            voting_item.save()

            count = int(request.POST.get('answers_count'))
            for i in range(count):
                answer_item = VotingAnswer(
                    text=request.POST.get('answer' + str(i)),
                    voting=voting_item
                )
                answer_item.save()

    return render(request, 'createvoting.html', context)


@login_required
def index(request):
    context = {}
    context['votings'] = Voting.objects.all()
    return render(request, 'index.html', context)


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
        'profile_form': profile_form,
        'title': 'Аккаунт пользователя'
    })
