# Generated by Django 3.0.3 on 2020-03-28 02:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobs', '0005_remove_job_interest_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedJob',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_qualified', models.BooleanField()),
                ('has_applied', models.BooleanField(default=False)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.Job')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='UserJob',
        ),
    ]