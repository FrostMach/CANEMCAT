# Generated by Django 5.1.3 on 2024-12-03 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0007_alter_intent_patterns_alter_intent_responses"),
    ]

    operations = [
        migrations.AlterField(
            model_name="intent",
            name="patterns",
            field=models.JSONField(default=""),
        ),
        migrations.AlterField(
            model_name="intent",
            name="responses",
            field=models.JSONField(default=""),
        ),
    ]
