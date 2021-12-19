# Generated by Django 3.2.7 on 2021-11-07 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=100)),
                ('assignment', models.CharField(default=' ', max_length=200)),
                ('deadline', models.DateField()),
                ('completed', models.BooleanField()),
            ],
        ),
    ]
