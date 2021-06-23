from django.shortcuts import render

#imported by me
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_302_FOUND
from .utils import send_otp_verification
from .utils import get_token
from django.utils import timezone

# Create your views here.

class RegisterView(APIView):
    permission_classes = ()
    def post(self, request):
        output_detail = 'Failed'
        output_status = False
        res_status = HTTP_400_BAD_REQUEST
        username = request.data.get('username', None)
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        if username and email and password: 
            obj = User.objects.filter(email=email).first()
            if obj:
                if obj.email_verified == True:
                  output_detail = 'User is allready exist with this email address!'
                else:
                    res_status = HTTP_302_FOUND
                    output_detail = 'You had allready initaited registration, a verification mail is sent, please proceed further.'
                    send_otp_verification(obj)
            else:  
                try:
                    User.objects.create(username=username, email=email)
                    user_obj = User.objects.get(username=username, email=email)
                    user_obj.set_password(password)
                    send_otp_verification(user_obj)
                    output_detail = 'Success'
                    output_status = True
                    res_status = HTTP_200_OK
                except Exception as e:
                    output_detail = str(e)
                
        else:
            output_detail = 'Requird fiels are missing!'
        context = {
            'status': output_status,
            'detail': output_detail,
        }

        return Response (context, status = res_status)

class VerificationView(APIView):
    permission_classes = ()
    def post(self, request):
        output_detail = 'Failed'
        output_status = False
        res_status = HTTP_400_BAD_REQUEST
        email = request.data.get('email', None)
        otp_code = request.data.get('otp_code', None)
        if email and otp_code:
            obj = User.objects.filter(email=email).first()
            if obj:
                if not obj.email_verified:
                    time_diff = timezone.now() - obj.otp_created_at
                    if time_diff.seconds < 300:
                        if obj.otp_code == otp_code:
                            obj.email_verified = True
                            obj.save()
                            output_detail = 'Success'
                            output_status = True
                            res_status = HTTP_200_OK
                        else:
                            output_detail = 'OTP does not match!'
                    else: 
                        output_detail = 'OTP is expired!'
                else:
                    output_detail = 'User is already verified!'
            else:
                output_detail = 'Invalid email is provided!'
        else:
            output_detail = 'Requird fiels are missing!'
        context = {
            'status': output_status,
            'detail': output_detail,
        }

        return Response (context, status = res_status)


class LoginView(APIView):
    permission_classes = ()
    def post(self, request):
        output_detail = 'failed'
        output_status = False
        data = {}
        res_status = HTTP_400_BAD_REQUEST
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        if email and password:
            obj = User.objects.filter(email=email).first()
            if obj:
                if obj.email_verified:
                    if obj.check_password(password):
                        data = get_token(obj)
                        output_detail = 'success'
                        output_status = True
                        res_status = HTTP_200_OK
                    else:
                        output_detail = 'Wrong password entered!'
                else:
                    res_status = HTTP_302_FOUND
                    output_detail = 'Email is not verified, an otp is sent on registered email. Please verify!'
            else:
                output_detail = 'Entered email does not exist. Please register first!'
        else:
            output_detail = 'Requird fiels are missing!'
        context = {
            'status': output_status,
            'detail': output_detail,
            'data': data
        }

        return Response (context, status = res_status)

