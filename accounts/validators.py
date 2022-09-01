from django.core.validators import RegexValidator

phone_number_validator = RegexValidator(regex=r'^(?:0|98|\+98|\+980|0098|098|00980)?(9\d{9})$',
                                        message="شماره تماس معتبر نیست.")
telegram_username_validator = RegexValidator(regex=r'^\w{5,32}$', message="آی‌دی تلگرام معتبر نیست.")

