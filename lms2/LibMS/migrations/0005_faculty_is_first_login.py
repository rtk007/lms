# Generated by Django 5.1 on 2024-08-18 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LibMS", "0004_faculty_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="faculty",
            name="is_first_login",
            field=models.BooleanField(default=True),
        ),
    ]
