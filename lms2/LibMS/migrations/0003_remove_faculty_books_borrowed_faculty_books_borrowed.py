# Generated by Django 5.1 on 2024-08-16 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LibMS", "0002_faculty_alter_book_author_alter_book_book_id_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="faculty",
            name="books_borrowed",
        ),
        migrations.AddField(
            model_name="faculty",
            name="books_borrowed",
            field=models.ManyToManyField(
                blank=True, related_name="borrowers", to="LibMS.book"
            ),
        ),
    ]
