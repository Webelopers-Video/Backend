from django.conf import settings
from rest_framework import serializers

from models import Video, Lesson, ArchivedFiles


class VideoSerializer(serializers.ModelSerializer):
    video_url = serializers.SerializerMethodField('_video_url')

    @staticmethod
    def _video_url(self, obj):
        if not obj.video_file:
            return None
        path = obj.video_file.url
        if settings.WEBELOPERS_DOMAIN not in path:
            return settings.WEBELOPERS_DOMAIN + path
        return path

    class Meta:
        model = Video
        fields = ['title', 'category', 'created_at', 'video_url']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title', 'professor', 'start_date']


class ArchivedFilesSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField('_file_url')

    @staticmethod
    def _file_url(self, obj):
        if not obj.file:
            return None
        path = obj.file.url
        if settings.WEBELOPERS_DOMAIN not in path:
            return settings.WEBELOPERS_DOMAIN + path
        return path

    class Meta:
        model = ArchivedFiles
        fields = ['file_url', 'title', 'description', 'type', 'lesson']
