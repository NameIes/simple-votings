import datetime
from django.shortcuts import render, HttpResponse

from .models import *
from .forms import AddVotingForm


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

    return HttpResponse('Ваш голос учитан!')


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


def bd_example(request):
    context = {'form': AddVotingForm()}

    if request.method == 'POST':
        form = AddVotingForm(request.POST)
        if form.is_valid():
            voting_item = Voting(text=form.data['question'],
                                 start=datetime.datetime.now())
            voting_item.save()

            answers = form.data['answers'].split('\n')
            for i in answers:
                if len(i) <= 200:
                    answer_item = VotingAnswer(text=i, voting=voting_item)
                    answer_item.save()

    votings = Voting.objects.all()
    lst = []
    for voting in votings:
        lst.append((voting, VotingAnswer.objects.filter(voting=voting)))

    if len(lst) > 0:
        context['data'] = lst

    return render(request, 'bd_example.html', context)
