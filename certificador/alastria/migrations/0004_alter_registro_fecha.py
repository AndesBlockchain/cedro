# Generated by Django 3.2 on 2021-04-19 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alastria', '0003_alter_registro_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registro',
            name='fecha',
            field=models.DateTimeField(),
        ),
    ]
