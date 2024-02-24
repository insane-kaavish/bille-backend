from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import *
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label="Email")
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


#Serializer to Get User Details using Django Token Authentication
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomUser
		fields = ["id", "first_name", "last_name", "email", "num_people", "ke_num"
			# , "num_stayathome", "num_parttime", "num_fulltime"
			]
    
#Serializer to Register User
class RegisterSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(
		required=True,
		validators=[UniqueValidator(queryset=CustomUser.objects.all())]
	)
	password = serializers.CharField(
		write_only=True, required=True, validators=[validate_password])
	password2 = serializers.CharField(write_only=True, required=True)
	class Meta:
		model = CustomUser
		fields = ('email', 'password', 'password2',
			'first_name', 'last_name', 'num_people',
			'ke_num'
			# , 'num_stayathome', 'num_parttime', 'num_fulltime'
			)
		extra_kwargs = {
			'first_name': {'required': True},
			'last_name': {'required': True}
			}
	def validate(self, attrs):
		if attrs['password'] != attrs['password2']:
			raise serializers.ValidationError(
				{"password": "Password fields didn't match."})
		return attrs
	def create(self, validated_data):
		user = CustomUser.objects.create(
			email= validated_data['email'],
			first_name= validated_data['first_name'],
			last_name= validated_data['last_name'],
			num_people= validated_data['num_people'],
			# num_stayathome= validated_data['num_stayathome'],
			# num_parttime= validated_data['num_parttime'],
			# num_fulltime= validated_data['num_fulltime']
			)
		user.set_password(validated_data['password'])
		user.save()
		return user