# Generated by Django 4.0.3 on 2022-03-25 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0013_alter_post_options_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='start_date',
            field=models.DateTimeField(verbose_name='Дата первой отправки'),
        ),
    ]
