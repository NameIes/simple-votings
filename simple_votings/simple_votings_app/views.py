from django.shortcuts import render
from .models import modelTest, Voting, VotingAnswer
from .forms import AddVotingForm


def viewtest(request):
    context = {}

    quest = modelTest.objects.get(id=1)
    quest.click_count += 1
    quest.save()

    context['question'] = quest

    return render(request,'base.html', context)


def bd_example(request):
    context = {'form': AddVotingForm()}

    if request.method == 'POST':
        form = AddVotingForm(request.POST)
        if form.is_valid():
            voting_item = Voting(text=form.data['question'])
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
