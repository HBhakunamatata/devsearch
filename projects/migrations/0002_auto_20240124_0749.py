# Generated by Django 3.2.4 on 2024-01-24 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='vote_ratio',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='vote_total',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
