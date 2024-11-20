# Generated by Django 5.1.3 on 2024-11-19 18:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AdoptionApplication",
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
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("P", "Pendiente"),
                            ("A", "Aprobada"),
                            ("D", "Denegada"),
                        ],
                        default="P",
                        max_length=1,
                    ),
                ),
                ("application_date", models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name="Animal",
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
                ("name", models.CharField(max_length=100)),
                ("age", models.PositiveIntegerField()),
                (
                    "species",
                    models.CharField(
                        choices=[("perro", "Perro"), ("gato", "Gato")], max_length=10
                    ),
                ),
                ("description", models.TextField()),
                ("image", models.ImageField(upload_to="animals/")),
                (
                    "adoption_status",
                    models.CharField(
                        choices=[
                            ("disponible", "Disponible"),
                            ("reservado", "Reservado"),
                            ("adoptado", "Adoptado"),
                        ],
                        default="disponible",
                        max_length=10,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Shelter",
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
                ("name", models.CharField(max_length=50, verbose_name="Nombre")),
                ("address", models.CharField(max_length=100, verbose_name="Dirección")),
                ("telephone", models.CharField(max_length=12, verbose_name="Teléfono")),
                (
                    "email",
                    models.EmailField(
                        max_length=100, verbose_name="Correo electrónico"
                    ),
                ),
                (
                    "accreditation_file",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="files/",
                        verbose_name="Documento acreditativo",
                    ),
                ),
                (
                    "accreditation_status",
                    models.BooleanField(
                        default=True, verbose_name="Estado de acreditación"
                    ),
                ),
                (
                    "register_date",
                    models.DateField(
                        blank=True, null=True, verbose_name="Fecha de registro"
                    ),
                ),
                (
                    "status",
                    models.BooleanField(blank=True, null=True, verbose_name="Estado"),
                ),
            ],
        ),
    ]