# Generated by Django 5.1.6 on 2025-02-20 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('typing_app', '0006_typinggameresult_alter_examtype_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='examcontent',
            name='passage_english',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='examcontent',
            name='passage_hindi',
            field=models.TextField(blank=True, null=True),
        ),
    ]
