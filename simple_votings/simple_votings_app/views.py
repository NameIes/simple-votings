from django.contrib.auth.models import User

from .models import Like, Comment, Profile
from .forms import AddCommentForm
# -*- coding: utf-8 -*-

from django.db import transaction
# https://django.fun/docs/ru/3.0/topics/db/transactions/

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Vote, VotingAnswer, Voting
from .forms import UserUpdateForm, ProfileUpdateForm

from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm

from PIL import Image
from django.core.files.storage import FileSystemStorage


@login_required
def voting(request, voting_id):
    context = {}
    context['voting'] = Voting.objects.get(id=voting_id)
    context['form'] = AddCommentForm()
    context['voted_answers'] = []

    for i in context['voting'].answers():
        for j in i.votes():
            if j.user == request.user:
                context['voted_answers'].append(i)

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
        if request.user not in [i.user for i in answer_item.votes()]:
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
        if request.user not in [i.user for i in voting_item.likes()]:
            like_item = Like(
                voting=voting_item,
                user=request.user
            )
            like_item.save()

    return redirect('/voting/' + str(voting_id))


def get_voting_errors(request):
    errors = []
    try:
        if not request.POST['question'].strip():
            errors.append('Поле опроса пустое')
        answers = request.POST.getlist('answer')
        if len(answers) < 2 or len(answers) > 25:
            errors.append('Неверное кол-во ответов')
        for i in answers:
            if not i.strip():
                errors.append('Не все поля ответов заполнены')
                break
    except KeyError:
        errors.append('Что-то не так, перезагрузите страницу')

    return errors


@login_required
def create_voting(request):
    context = {}

    if request.method == 'POST':
        context['errors'] = get_voting_errors(request)

        if len(context['errors']) == 0:
            voting_item = Voting(
                text=request.POST['question'].strip(),
                user=request.user
            )
            if request.POST.get('end_time'):
                voting_item.end_time = request.POST.get('end_time')
            if request.POST.get('is_multiple', None) is not None:
                voting_item.is_multiple = True
            voting_item.save()

            for answer in request.POST.getlist('answer'):
                answer_item = VotingAnswer(
                    text=answer,
                    voting=voting_item
                )
                answer_item.save()
        return redirect('/voting/' + str(voting_item.id))

    return render(request, 'createvoting.html', context)


@login_required
def voting_edit(request, voting_id):
    context = {}
    context['voting'] = Voting.objects.get(id=voting_id)

    if request.method == 'POST':
        context['errors'] = get_voting_errors(request)

        if len(context['errors']) == 0:
            voting_item = Voting.objects.get(id=voting_id)
            question = request.POST['question']
            answers = request.POST.getlist('answer')
            end_time = request.POST['end_time']
            is_multiple = request.POST.get('is_multiple', None)

            if voting_item.text != question:
                voting_item.text = question
                for answer in voting_item.answers():
                    for vote in answer.votes():
                        vote.delete()
                for like_item in voting_item.likes():
                    like_item.delete()

            if not end_time:
                voting_item.end_time = None
            else:
                voting_item.end_time = end_time

            if is_multiple is None:
                voting_item.is_multiple = False
            else:
                voting_item.is_multiple = True
            voting_item.save()

            for answer_item in voting_item.answers():
                if answer_item.text not in answers:
                    answer_item.delete()

            for answer_item in voting_item.answers():
                if answer_item.text in answers:
                    answers.remove(answer_item.text)

            for answer_text in answers:
                answer_item = VotingAnswer(
                    text=answer_text,
                    voting=voting_item
                )
                answer_item.save()

            return redirect('/voting/' + str(voting_id))

    return render(request, 'voting_edit.html', context)


@login_required
def delete_voting(request, voting_id):
    if request.method == 'POST':
        voting = Voting.objects.get(id=voting_id)
        if request.user == voting.user:
            voting.delete()

    return redirect('/')


@login_required
def index(request):
    context = {}
    context['votings'] = Voting.objects.all()
    return render(request, 'index.html', context)


def profile(request, user_id):
    context = {}
    context['ufp'] = User.objects.get(id=user_id)
    context['profile'] = Profile.objects.get(user=user_id)

    return render(request, 'profile.html', context)


@login_required
@transaction.atomic
def edit_profile(request, user_id):
    context = {}
    context['ufp'] = User.objects.get(id=user_id)
    context['profile'] = Profile.objects.get(user=user_id)
    context['errors'] = []
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=User.objects.get(id=user_id))
        p = Profile.objects.get(user=user_id)
        try:
            image = request.FILES['avatar']
            if image.size <= 5000000:
                if image.content_type.split('/')[0] == 'image':
                    # Get file extension
                    i = -1
                    while image.name[i] != '.':
                        i -= 1
                    path = 'avatars/' + str(user_id) + image.name[i:]

                    # Init
                    fs = FileSystemStorage()

                    # Remove old avatar
                    if p.avatar.name != 'avatars/0.png':
                        fs.delete(p.avatar.path)

                    # Save avatar
                    fs.save(path, image)
                    p.avatar = path
                    p.save()

                    # Resize
                    image = Image.open(p.avatar)
                    size = (200, 200)
                    image = image.resize(size, Image.ANTIALIAS)
                    image.save(p.avatar.path)
                else:
                    pass
            else:
                pass
        except Exception:
            pass
        p.show_email = False if request.POST.get('show_email') is None else True
        p.save()
        profile_form = ProfileUpdateForm(request.POST, instance=Profile.objects.get(user=user_id))
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('/profile/' + str(user_id))
    else:
        user_form = UserUpdateForm(instance=User.objects.get(id=user_id))
        profile_form = ProfileUpdateForm(instance=Profile.objects.get(user=user_id))
    context['user_form'] = user_form
    context['profile_form'] = profile_form
    return render(request, 'profile_edit.html', context)


# https://ustimov.org/posts/17/
class RegisterFormView(FormView):
    form_class = UserCreationForm
    # Ссылка, на которую будет перенаправляться user
    # в случае успешной регистрации
    success_url = "/login/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "register.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()
        for key in form.fields:
            print(form.fields[key])

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)
