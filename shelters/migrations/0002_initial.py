# Generated by Django 5.1.3 on 2024-12-16 09:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("shelters", "0001_initial"),
        ("users", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="adoptionapplication",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.adopterprofile",
            ),
        ),
        migrations.AddField(
            model_name="adoptionapplication",
            name="animal",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="shelters.animal",
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="events",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="animal",
            name="shelter",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="animals",
                to="shelters.shelter",
                verbose_name="Protectora",
            ),
        ),
        migrations.AddField(
            model_name="adoptionapplication",
            name="shelter",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="shelters.shelter",
            ),
        ),
    ]
