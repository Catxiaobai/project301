# Generated by Django 3.1.1 on 2020-10-25 02:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newfirst', '0011_auto_20201024_2204'),
    ]

    operations = [
        migrations.CreateModel(
            name='Design',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, default='')),
                ('describe', models.TextField(default='')),
                ('type', models.TextField(default='')),
                ('element', models.TextField(default='')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newfirst.item')),
            ],
        ),
        migrations.CreateModel(
            name='DesignCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apply', models.TextField(blank=True, default='')),
                ('suitable', models.TextField(blank=True, default='')),
                ('problem', models.TextField(blank=True, default='')),
                ('design', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='newfirst.design')),
            ],
        ),
        migrations.RenameField(
            model_name='designcriteria',
            old_name='remark',
            new_name='element',
        ),
        migrations.AlterField(
            model_name='demand',
            name='fmea',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='newfirst.fmea'),
        ),
        migrations.AlterField(
            model_name='designcriteria',
            name='name',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.CreateModel(
            name='DesignComplete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complete', models.TextField(blank=True, default='')),
                ('designCheck', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='newfirst.designcheck')),
            ],
        ),
    ]
