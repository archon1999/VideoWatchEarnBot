# Generated by Django 4.0.3 on 2022-03-25 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_alter_video_managers_botuser_is_admin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='botuser',
            name='invited',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='referalss', to='backend.botuser', verbose_name='Кто пригласил'),
        ),
    ]
