# Generated by Django 3.2.6 on 2021-08-23 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='title',
            field=models.CharField(choices=[('Software Engineer', 'Software Engineer'), ('Data Scientist', 'Data Scientist')], default='Software Engineer', max_length=50),
        ),
    ]
