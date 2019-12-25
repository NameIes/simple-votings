# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Voting(models.Model):
    text = models.CharField(max_length=500)
    start_time = models.DateTimeField(auto_now=True)
    end_time = models.DateTimeField(null=True, default=None)

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % (self.text)

    def __unicode__(self):
        return u'%s' % (self.text)

    def answers(self):
        return VotingAnswer.objects.filter(voting=self)

    def like(self):
        return "/like/" + str(self.id)

    def likes(self):
        return Like.objects.filter(voting=self)

    def likes_count(self):
        return len(self.likes())

    def comments(self):
        return Comment.objects.filter(voting=self)


class Like(models.Model):
    date = models.DateTimeField(auto_now=True)

    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)


class VotingAnswer(models.Model):
    text = models.CharField(max_length=500)

    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.text

    def action(self):
        return "/vote/" + str(self.id)

    def votes(self):
        return Vote.objects.filter(answer=self)

    def votes_count(self):
        return len(self.votes())


class Vote(models.Model):
    date = models.DateTimeField(auto_now=True)

    answer = models.ForeignKey(to=VotingAnswer, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)


class Comment(models.Model):
    date = models.DateTimeField(auto_now=True)
    text = models.CharField(max_length=500)

    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)


class Example(models.Model):
    number = models.IntegerField(default=1)
    date = models.DateTimeField()
    text = models.CharField(max_length=200)
    galochka = models.BooleanField(blank=False)


class ExampleAdmin(admin.ModelAdmin):
    list_display = ('number', 'date', 'text', 'galochka')


class VotingAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'start_time', 'end_time')


class VotingAnswerAdmin(admin.ModelAdmin):
    list_display = ('text', )


class Profile(models.Model):
    """Profile
    Base User Model

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    # TODO: Аватар, История(созданные голосования, лайки, голоса, жалобы)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


admin.site.register(Example, ExampleAdmin)
admin.site.register(Voting, VotingAdmin)
admin.site.register(VotingAnswer, VotingAnswerAdmin)
