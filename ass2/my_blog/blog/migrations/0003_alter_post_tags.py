# Generated by Django 5.1.1 on 2024-10-06 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_userprofile_remove_user_groups_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='blog.tag'),
        ),
    ]
