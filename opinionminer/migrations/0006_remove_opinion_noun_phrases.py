# Generated by Django 3.2 on 2023-06-15 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opinionminer', '0005_opinion_noun_phrases'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='opinion',
            name='noun_phrases',
        ),
    ]
