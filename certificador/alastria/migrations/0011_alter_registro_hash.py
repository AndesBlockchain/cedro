# Generated by Django 5.0.4 on 2024-05-06 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("alastria", "0010_estado"),
    ]

    operations = [
        migrations.AlterField(
            model_name="registro",
            name="hash",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
