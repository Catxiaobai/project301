# Generated by Django 3.1.1 on 2020-10-31 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newfirst', '0019_fmea_ignore'),
    ]

    operations = [
        migrations.AddField(
            model_name='design',
            name='belong',
            field=models.TextField(default=''),
        ),
    ]