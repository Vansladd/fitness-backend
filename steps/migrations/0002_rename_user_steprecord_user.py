# Generated by Django 4.2.20 on 2025-03-30 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("steps", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="steprecord",
            old_name="User",
            new_name="user",
        ),
    ]
