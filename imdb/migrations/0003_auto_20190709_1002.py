# Generated by Django 2.2.3 on 2019-07-09 04:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imdb', '0002_auto_20190708_1855'),
    ]

    operations = [
        migrations.RenameField(
            model_name='moviecast',
            old_name='actor',
            new_name='cast',
        ),
    ]
