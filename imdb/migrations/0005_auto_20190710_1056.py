# Generated by Django 2.2.3 on 2019-07-10 05:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imdb', '0004_movierating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movierating',
            old_name='ratings',
            new_name='rating',
        ),
    ]
