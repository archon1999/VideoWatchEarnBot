# Generated by Django 4.0.3 on 2022-03-19 10:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_template_title_verbose_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='botuser',
            name='bot_state',
            field=models.IntegerField(choices=[(0, 'Nothing')], default=0),
        ),
        migrations.AddField(
            model_name='botuser',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Создано'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='botuser',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='video',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Создано'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='template',
            name='body',
            field=models.TextField(verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='template',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Название для разработки'),
        ),
        migrations.AlterField(
            model_name='template',
            name='title_verbose_name',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='template',
            name='type',
            field=models.IntegerField(choices=[(1, 'Сообщение'), (2, 'Кнопка'), (3, 'Смайлик')], verbose_name='Тип'),
        ),
    ]
