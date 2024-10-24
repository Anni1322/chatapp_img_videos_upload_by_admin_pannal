# Generated by Django 5.1.2 on 2024-10-22 19:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_message', models.TextField(verbose_name='user_Message')),
                ('answers', models.TextField(verbose_name='answers')),
            ],
        ),
        migrations.CreateModel(
            name='MediaModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_path', models.ImageField(blank=True, max_length=200, null=True, upload_to='Images/images')),
                ('video_path', models.FileField(blank=True, max_length=200, null=True, upload_to='Videos/videos')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media', to='chat.questionmodel')),
            ],
        ),
    ]
