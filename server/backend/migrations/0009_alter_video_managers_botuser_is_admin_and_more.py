# Generated by Django 4.0.3 on 2022-03-25 09:54

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_rename_viewed_viewvideo_received'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='video',
            managers=[
                ('videos', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='botuser',
            name='is_admin',
            field=models.BooleanField(default=False, verbose_name='Админ?'),
        ),
        migrations.AlterField(
            model_name='botuser',
            name='referals',
            field=models.ManyToManyField(blank=True, to='backend.botuser', verbose_name='Рефералы'),
        ),
        migrations.AlterField(
            model_name='template',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Название (для разработчика)'),
        ),
        migrations.AlterField(
            model_name='template',
            name='type',
            field=models.IntegerField(choices=[(1, 'Сообщение'), (2, 'Кнопка'), (3, 'Смайлик')], verbose_name='Тип (для разработчика)'),
        ),
        migrations.AlterField(
            model_name='viewvideo',
            name='received',
            field=models.BooleanField(default=False, verbose_name='Получен бонус?'),
        ),
        migrations.AlterField(
            model_name='viewvideo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='backend.botuser', verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='viewvideo',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='backend.video', verbose_name='Видео'),
        ),
    ]