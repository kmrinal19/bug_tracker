# Generated by Django 3.0.5 on 2020-06-10 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0020_auto_20200531_2223'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='issue',
            options={'ordering': ['-created_on']},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-created_on']},
        ),
    ]