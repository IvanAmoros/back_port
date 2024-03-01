from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import json
from .models import TechnicalSkillCategory, TechnicalSkill, WorkExperience
from rest_framework import permissions, status
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import TechnicalSkillCategorySerializer, TechnicalSkillSerializer, WorkExperienceSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAdminUser, AllowAny


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
	def validate(self, attrs):
		data = super().validate(attrs)
		# Add extra responses here, e.g. user information
		data['username'] = self.user.username
		data['email'] = self.user.email
		# You can add more fields as needed
		return data

class MyTokenObtainPairView(TokenObtainPairView):
	serializer_class = MyTokenObtainPairSerializer


class ValidateTokenView(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request):
		try:
			# Assuming the token is already validated by IsAuthenticated permission
			user = request.user
			return Response({
				'username': user.username,
				'email': user.email,
				# Add any other user details you want to return
			})
		except Exception as e:
			return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)


class TechnicalSkillCategoryList(ListAPIView):
	queryset = TechnicalSkillCategory.objects.all()
	serializer_class = TechnicalSkillCategorySerializer
	permission_classes = [AllowAny]


class TechnicalSkillCategoryCreate(CreateAPIView):
	queryset = TechnicalSkillCategory.objects.all()
	serializer_class = TechnicalSkillCategorySerializer
	permission_classes = [IsAdminUser]


class TechnicalSkillCreate(CreateAPIView):
	queryset = TechnicalSkill.objects.all()
	serializer_class = TechnicalSkillSerializer
	permission_classes = [IsAdminUser]


class TechnicalSkillUpdate(RetrieveUpdateAPIView):
	queryset = TechnicalSkill.objects.all()
	serializer_class = TechnicalSkillSerializer
	permission_classes = [IsAuthenticated, IsAdminUser]


class TechnicalSkillCategoryUpdate(RetrieveUpdateAPIView):
	queryset = TechnicalSkillCategory.objects.all()
	serializer_class = TechnicalSkillCategorySerializer
	permission_classes = [IsAuthenticated, IsAdminUser]
 

class WorkExperienceList(ListAPIView):
	queryset = WorkExperience.objects.all().order_by('-from_date')
	serializer_class = WorkExperienceSerializer
	permission_classes = [AllowAny]