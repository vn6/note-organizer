# Generated by Django 3.2.7 on 2021-11-11 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0005_notes_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='pref_cal_view',
        ),
    ]