# Generated by Django 5.0.4 on 2024-05-16 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("alastria", "0012_alter_registro_comprobante"),
    ]

    operations = [
        migrations.AddField(
            model_name="estado",
            name="last_sent_nonce",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="registro",
            name="comprobante",
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name="registro",
            name="hash",
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
