# Generated by Django 2.2 on 2021-11-15 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='faved_by',
            field=models.ManyToManyField(null=True, related_name='fav_books', to='books_app.User'),
        ),
    ]
