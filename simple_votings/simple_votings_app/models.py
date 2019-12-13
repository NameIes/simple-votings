from django.db import models


class modelTest(models.Model):
    question = models.CharField(max_length=50)
    click_count = models.IntegerField()


class Voting(models.Model):
    text = models.CharField(max_length=200)
    likes = models.IntegerField(default=0)
    start = models.DateTimeField()
    # TODO: Добавить дату окончания


class VotingAnswer(models.Model):
    text = models.CharField(max_length=200)
    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE)
    votes_count = models.IntegerField(default=0)


# TODO: Добавить модель комментариев