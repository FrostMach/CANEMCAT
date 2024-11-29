# Generated by Django 4.1 on 2024-11-27 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shelters", "0003_adoptionapplication_shelter"),
    ]

    operations = [
        migrations.AddField(
            model_name="shelter",
            name="latitude",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="shelter",
            name="longitude",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
