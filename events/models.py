from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from accounts.models import User


class Event(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    details = models.TextField()
    enroll_start_time = models.DateTimeField()
    enroll_end_time = models.DateTimeField()
    start_date = models.DateField()
    end_date = models.DateField()
    site_url = models.URLField()
    staffs = models.ManyToManyField(User, related_name='staff_events')
    participants = models.ManyToManyField(
        User,
        through='EventEnrollment',
        through_fields=('event', 'participant'),
        related_name='participant_events'
    )


class EventEnrollment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    goal = models.TextField(null=True)
    goal_achieved = models.BooleanField(null=True)
    rating = models.IntegerField(null=True, validators=[MinValueValidator(1), MaxValueValidator(5)])

