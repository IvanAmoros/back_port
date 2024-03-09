from .models import Comment, TechnicalSkillCategory, TechnicalSkill, WorkExperience, Studie
from .serializers import TechnicalSkillCategorySerializer, TechnicalSkillSerializer, WorkExperienceSerializer, StudieSerializer, CommentSerializer

from rest_framework import status
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
	def validate(self, attrs) -> dict[str, str]:
		data = super().validate(attrs)
		data['username'] = self.user.username
		data['email'] = self.user.email
		data['is_superuser'] = self.user.is_superuser
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
	queryset = TechnicalSkillCategory.objects.all().order_by('id')
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
	permission_classes = [IsAdminUser]


class TechnicalSkillCategoryUpdate(RetrieveUpdateAPIView):
	queryset = TechnicalSkillCategory.objects.all()
	serializer_class = TechnicalSkillCategorySerializer
	permission_classes = [IsAdminUser]
 

class WorkExperienceList(ListAPIView):
	queryset = WorkExperience.objects.all().order_by('-from_date')
	serializer_class = WorkExperienceSerializer
	permission_classes = [AllowAny]


class StudieList(ListAPIView):
	queryset = Studie.objects.all().order_by('-from_date')
	serializer_class = StudieSerializer
	permission_classes = [AllowAny]


class CommentList(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            return Comment.objects.all().order_by('created')
        else:
            return Comment.objects.filter(accepted=True).order_by('created')

    def perform_create(self, serializer):
        serializer.save()