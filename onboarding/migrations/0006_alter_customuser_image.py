# Generated by Django 3.2.6 on 2021-08-24 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0005_alter_customuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='image',
            field=models.ImageField(blank=True, default='user_photos/github-icon-38988.png', upload_to='user_photos/'),
        ),
    ]
