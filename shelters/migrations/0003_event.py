# Generated by Django 5.1.3 on 2024-12-09 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shelters", "0002_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("start", models.DateField()),
                ("end", models.DateField(blank=True, null=True)),
            ],
        ),
    ]
