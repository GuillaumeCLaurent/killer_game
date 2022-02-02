# Generated by Django 4.0.1 on 2022-01-25 15:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('killer_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={},
        ),
        migrations.RemoveField(
            model_name='game',
            name='players',
        ),
        migrations.RemoveField(
            model_name='player',
            name='name',
        ),
        migrations.AddField(
            model_name='game',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='player',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
