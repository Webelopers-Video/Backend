from rest_framework import serializers

from models import Event, EventEnrollment
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    # for ManyToMany Fields
    staffs = UserSerializer(read_only=True, many=True)
    participants = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Event
        fields = '__all__'


class EventEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventEnrollment
        fields = '__all__'
