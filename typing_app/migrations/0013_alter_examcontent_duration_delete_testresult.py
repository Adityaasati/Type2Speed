# Generated by Django 5.1.6 on 2025-02-27 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('typing_app', '0012_remove_examcontent_instructions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examcontent',
            name='duration',
            field=models.IntegerField(default=15, help_text='Duration in minutes'),
        ),
        migrations.DeleteModel(
            name='TestResult',
        ),
    ]
