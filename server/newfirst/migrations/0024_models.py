# Generated by Django 3.1.1 on 2020-11-08 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newfirst', '0023_auto_20201102_0916'),
    ]

    operations = [
        migrations.CreateModel(
            name='Models',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='')),
                ('scenes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newfirst.scenes')),
            ],
        ),
    ]
