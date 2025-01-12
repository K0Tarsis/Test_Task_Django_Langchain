# Generated by Django 5.1.4 on 2025-01-12 18:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='homes',
            name='area',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='homes',
            name='title',
            field=models.CharField(default=None, max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='homes',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='homes',
            name='bathrooms',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='homes',
            name='bedrooms',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='homes',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('sender', models.CharField(choices=[('user', 'User'), ('bot', 'Bot')], max_length=10)),
                ('message', models.TextField()),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat_bot.chat')),
            ],
        ),
    ]