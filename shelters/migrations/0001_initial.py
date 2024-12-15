# Generated by Django 5.1.3 on 2024-12-15 00:14

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
                ("name", models.CharField(max_length=100, verbose_name="Nombre")),
                (
                    "species",
                    models.CharField(
                        choices=[("perro", "Perro"), ("gato", "Gato")],
                        max_length=10,
                        verbose_name="Especie",
                    ),
                ),
                (
                    "sex",
                    models.CharField(
                        choices=[("macho", "Macho"), ("hembra", "Hembra")],
                        default="Macho",
                        max_length=10,
                    ),
                ),
                ("age", models.PositiveIntegerField()),
                (
                    "size",
                    models.CharField(
                        choices=[
                            ("grande", "Grande"),
                            ("mediano", "Mediano"),
                            ("pequeño", "Pequeño"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "personality",
                    models.CharField(
                        choices=[
                            ("sociable", "Sociable"),
                            ("protector", "Protector"),
                            ("independiente", "Independiente"),
                        ],
                        max_length=15,
                    ),
                ),
                (
                    "energy",
                    models.CharField(
                        choices=[
                            ("activo", "Activo"),
                            ("moderado", "Moderado"),
                            ("tranquilo", "Tranquilo"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "fur",
                    models.CharField(
                        choices=[("largo", "Largo"), ("corto", "Corto")], max_length=10
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
                        default="Disponible",
                        max_length=10,
                    ),
                ),
                ("features", models.BinaryField(blank=True, null=True)),
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
                        auto_now_add=True, null=True, verbose_name="Fecha de registro"
                    ),
                ),
                (
                    "status",
                    models.BooleanField(blank=True, null=True, verbose_name="Estado"),
                ),
                (
                    "latitude",
                    models.FloatField(blank=True, null=True, verbose_name="Latitud"),
                ),
                (
                    "longitude",
                    models.FloatField(blank=True, null=True, verbose_name="Longitud"),
                ),
                (
                    "postal_code",
                    models.CharField(
                        blank=True,
                        max_length=10,
                        null=True,
                        verbose_name="Código Postal",
                    ),
                ),
            ],
        ),
    ]
