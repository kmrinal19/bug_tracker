# Generated by Django 3.0.5 on 2020-05-18 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0011_user_userid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='UserId',
            new_name='userId',
        ),
    ]