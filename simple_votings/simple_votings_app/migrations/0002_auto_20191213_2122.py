# Generated by Django 3.0 on 2019-12-13 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_votings_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='voting',
            name='ends',
            field=models.DateField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='voting',
            name='like_count',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='voting',
            name='started',
            field=models.DateField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='votinganswer',
            name='votes_count',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
    ]