# Generated by Django 3.0 on 2019-12-17 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_votings_app', '0009_example'),
    ]

    operations = [
        migrations.AlterField(
            model_name='example',
            name='date',
            field=models.DateTimeField(),
        ),
    ]