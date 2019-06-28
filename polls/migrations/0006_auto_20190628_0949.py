# Generated by Django 2.2.2 on 2019-06-28 04:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_remove_choice_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fruit',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='choice',
            name='shirt_size',
        ),
        migrations.AddField(
            model_name='choice',
            name='choice_text',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='polls.Question'),
            preserve_default=False,
        ),
    ]
