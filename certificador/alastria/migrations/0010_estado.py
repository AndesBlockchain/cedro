# Generated by Django 5.0.4 on 2024-05-02 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("alastria", "0009_registro_estado"),
    ]

    operations = [
        migrations.CreateModel(
            name="Estado",
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
                ("estado", models.CharField(max_length=20)),
                ("contador", models.IntegerField(default=0)),
            ],
        ),
    ]