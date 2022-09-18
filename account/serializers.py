from sys import api_version
from xml.dom import ValidationErr
from rest_framework import serializers
from account.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Util


class UserRegistrationSerializer(serializers.ModelSerializer):
    cnfm_password = serializers.CharField(style={'input_type':'password'},write_only = True)
    class Meta:
        model = User
        fields = ['email','password','cnfm_password','name','gender','date_of_birth','doctor_name','caretaker_relation']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate(self, attrs):
        password = attrs.get('password')
        cnfm_password = attrs.get('cnfm_password')
        if password != cnfm_password:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 100)
    class Meta:
        model = User
        fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','name','date_of_birth','caretaker_relation','doctor_name']

class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, style = {'input_type': 'password'}, write_only=True)
    cnfm_password = serializers.CharField(max_length=100, style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['password', 'cnfm_password']

    def validate(self, attrs):
        password = attrs.get('password')
        cnfm_password = attrs.get('cnfm_password')
        user = self.context.get('user')
        if password != cnfm_password:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email = email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)
            link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
            print('Password Reset Link', link)

            #Send Email
            body = 'Click Following Link to Reset Your Password '+link
            data = {
                'subject': 'Reset Your DementiCare Password',
                'body': body,
                'to_email': user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise ValidationErr('Your are not a Registered User')

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100, style = {'input_type': 'password'}, write_only=True)
    cnfm_password = serializers.CharField(max_length=100, style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['password', 'cnfm_password']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            cnfm_password = attrs.get('cnfm_password')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != cnfm_password:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise serializers.ValidationError('Token is not Valid or Expired')
    
