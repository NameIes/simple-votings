from django.db import models


class modelTest(models.Model):
    question = models.CharField(max_length=50)
    click_count = models.IntegerField()


class Voting(models.Model):
    text = models.CharField(max_length=200)
    # TODO: Добавить ещё поля (комментарии, лайки, дата начала/конца)


class VotingAnswer(models.Model):
    text = models.CharField(max_length=200)
    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE)
    # TODO: Добавиь ещё поле кол-ва голосований

