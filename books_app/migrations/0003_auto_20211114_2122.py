# Generated by Django 2.2 on 2021-11-15 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0002_auto_20211114_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='faved_by',
            field=models.ManyToManyField(related_name='fav_books', to='books_app.User'),
        ),
    ]
