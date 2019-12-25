from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import VotingAnswer, Voting, Vote, Like, Comment
from .forms import AddVotingForm, AddCommentForm


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
