# Generated by Django 3.1.1 on 2023-05-20 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opinionminer', '0002_auto_20230515_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='opinion',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
