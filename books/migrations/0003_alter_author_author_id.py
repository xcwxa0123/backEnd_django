# Generated by Django 4.1.7 on 2023-04-16 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_alter_book_last_time_alter_episode_refresh_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='author_id',
            field=models.TextField(primary_key=True, serialize=False),
        ),
    ]
