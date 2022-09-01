import datetime
import secrets

from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMessage
from django.db import models
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from accounts import validators


class User(AbstractUser):
    phone_number = models.CharField('شماره تماس', validators=[validators.phone_number_validator], max_length=17, null=True, blank=True)
    profile_picture = models.ImageField('تصویر پروفایل', upload_to='user_profile_pictures', null=True, blank=True,
                                        default='user_profile_pictures/default.jpg')
    updated_at = models.DateTimeField('آخرین به‌روزرسانی', auto_now=True)

    def send_activation_email(self, domain):
        activate_user_token = ActivateUserToken(
            token=secrets.token_urlsafe(32),
            uid=urlsafe_base64_encode(force_bytes(self.id)),
        )
        activate_user_token.save()

        context = {
            'name': f"{self.first_name} {self.last_name}",
            'domain': domain,
            'uid': activate_user_token.uid,
            'token': activate_user_token.token,
        }

        msg_html = render_to_string('accounts/emails/activation.html', context)
        subject = 'فعال‌سازی حساب کاربری SSC'
        email = EmailMessage(subject, msg_html, to=[self.email])
        email.send()

    @classmethod
    def activate(cls, uid, token):
        activate_user_token = get_object_or_404(ActivateUserToken,
                                                uid=uid, token=token)

        user_id = urlsafe_base64_decode(uid).decode('utf-8')
        user = cls.objects.get(id=user_id)
        user.is_active = True
        activate_user_token.delete()
        user.save()


def next_year():
    return timezone.now() + datetime.timedelta(days=365)


class CoreMemberProfile(models.Model):
    class Role(models.TextChoices):
        HEAD = 'H', 'دبیر'
        VICE_HEAD = 'VH', 'نایب دبیر'
        PUBLIC_RELATIONS = 'PUR', 'روابط عمومی'
        DOCUMENTATION = 'DOC', 'مستندات'
        FINANCIAL = 'FI', 'مالی'
        PROPERTY = 'PRO', 'اموال'
        SYSTEMS = 'SY', 'سیستم‌ها'
        CENTRAL = 'CN', 'عضو مرکزی'
        UNDEFINED = 'UD', 'نامشخص'

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=next_year)
    role = models.CharField('مسئولیت', choices=Role.choices, max_length=3, default=Role.UNDEFINED)


class ProfessorProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=next_year)
    description = models.TextField('توضیحات')


class ActivateUserToken(models.Model):
    uid = models.CharField(max_length=100, null=True)
    token = models.CharField(max_length=100)
