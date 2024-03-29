# Generated by Django 2.2.2 on 2019-06-28 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_ox_person1'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='shirt_size',
            field=models.CharField(choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large')], default=1, max_length=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(max_length=60),
        ),
    ]
