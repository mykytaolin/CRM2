# Generated by Django 5.0 on 2024-01-19 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_userprofile_agent_organisation'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_agent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_organiser',
            field=models.BooleanField(default=True),
        ),
    ]