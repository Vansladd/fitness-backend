# Generated by Django 4.2.20 on 2025-03-31 08:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("steps", "0003_alter_steprecord_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="steprecord",
            name="date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
