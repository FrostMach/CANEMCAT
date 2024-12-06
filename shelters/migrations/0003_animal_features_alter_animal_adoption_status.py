# Generated by Django 4.1 on 2024-12-05 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shelters", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="animal",
            name="features",
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="animal",
            name="adoption_status",
            field=models.CharField(
                choices=[
                    ("disponible", "Disponible"),
                    ("reservado", "Reservado"),
                    ("adoptado", "Adoptado"),
                ],
                default="Disponible",
                max_length=10,
            ),
        ),
    ]