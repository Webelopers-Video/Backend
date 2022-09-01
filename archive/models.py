from django.core.validators import FileExtensionValidator
from django.db import models

from accounts.models import ProfessorProfile


class VideoCategory(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()


class Video(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(VideoCategory, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    video_file = models.FileField(upload_to='archive/videos', null=True,
                                  validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])


class Lesson(models.Model):
    title = models.CharField(max_length=50)
    professor = models.ForeignKey(ProfessorProfile, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    start_date = models.DateField()


class ArchivedFiles(models.Model):
    class Type(models.TextChoices):
        PROJECT = 'PRJ', 'پروژه'
        QUIZ = 'QZ', 'کوئیز'
        PRACTICE = 'PRA', 'تمرین'
        EXAM = 'EX', 'امتحان'
        UNDEFINED = 'UD', 'نامشخص'

    file = models.FileField(upload_to='archive/files', null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField('دسته‌بندی', choices=Type.choices, max_length=3, default=Type.UNDEFINED)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, default=None)

