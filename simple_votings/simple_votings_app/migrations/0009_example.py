# Generated by Django 3.0 on 2019-12-17 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_votings_app', '0008_auto_20191213_2154'),
    ]

    operations = [
        migrations.CreateModel(
            name='Example',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=1)),
                ('date', models.DateTimeField(auto_now=True)),
                ('text', models.CharField(max_length=200)),
                ('galochka', models.BooleanField()),
            ],
        ),
    ]