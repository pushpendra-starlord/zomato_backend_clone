from django.utils import timezone
from django.utils.crypto import get_random_string
from django.conf import settings
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken

def send_otp_verification(user_obj):
    otp_code = get_random_string(length=6, allowed_chars='1234567890')
    user_obj.otp_code = otp_code
    user_obj.otp_created_at = timezone.now()
    user_obj.save()
    subject = 'Account Verification'
    message = f'Hi {user_obj.username}, This mail consist of an OTP code. Please enter the otp code for verification of your account. OTP: {otp_code} '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_obj.email, ]
    send_mail( subject, message, email_from, recipient_list)

def get_token(user_object):
    refresh = RefreshToken.for_user(user_object)
    token = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    return token