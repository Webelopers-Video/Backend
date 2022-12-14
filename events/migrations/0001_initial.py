# Generated by Django 4.1 on 2022-08-30 18:50

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=150)),
                ('details', models.TextField()),
                ('enroll_start_time', models.DateTimeField()),
                ('enroll_end_time', models.DateTimeField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('site_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='EventEnrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('goal', models.TextField(null=True)),
                ('goal_achieved', models.BooleanField(null=True)),
                ('rating', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(related_name='participant_events', through='events.EventEnrollment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='staffs',
            field=models.ManyToManyField(related_name='staff_events', to=settings.AUTH_USER_MODEL),
        ),
    ]
