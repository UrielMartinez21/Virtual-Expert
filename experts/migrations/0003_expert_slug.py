# Generated by Django 5.2.3 on 2025-06-25 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experts', '0002_expert_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='expert',
            name='slug',
            field=models.SlugField(default='', max_length=100),
        ),
    ]
