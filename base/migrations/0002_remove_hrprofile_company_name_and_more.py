# Generated by Django 5.0.3 on 2024-04-02 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hrprofile',
            name='company_name',
        ),
        migrations.RemoveField(
            model_name='hrprofile',
            name='location',
        ),
    ]
