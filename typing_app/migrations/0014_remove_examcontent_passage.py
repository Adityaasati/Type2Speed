# Generated by Django 5.1.6 on 2025-03-01 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('typing_app', '0013_alter_examcontent_duration_delete_testresult'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examcontent',
            name='passage',
        ),
    ]
