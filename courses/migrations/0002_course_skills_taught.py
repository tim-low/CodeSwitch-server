# Generated by Django 3.0.3 on 2020-03-19 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0001_initial'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='skills_taught',
            field=models.ManyToManyField(to='skills.Skill'),
        ),
    ]
