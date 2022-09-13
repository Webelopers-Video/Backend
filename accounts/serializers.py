from curses.ascii import US
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from models import User, CoreMemberProfile, ProfessorProfile


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(style={'input_type': 'password'})
    new_password1 = serializers.CharField(style={'input_type': 'password'})
    new_password2 = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError(_('passwords don\'t match!'))
        if not self.context['request'].user.check_password(
                data['old_password']):
            raise serializers.ValidationError(_('invalid old password'))
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(
            raw_password=self.validated_data['new_password1']
        )
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['email', 'phone_number', 'updated_at', 'profile_picture']


class CoreMemberProfileSerializer(serializers.ModelSerializer):
    user_info = UserSerializer()

    class Meta:
        model = CoreMemberProfile
        fields = ['user_info', 'start_date', 'end_date', 'role']

class ProfessorProfileSerializer(serializers.ModelSerializer):
    user_info = UserSerializer()
    class Meta:
        model = ProfessorProfile
        fields = ['user_info', 'start_date', 'end_date', 'description']
