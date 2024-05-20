from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated

from .models import Comment, TechnicalSkillCategory, TechnicalSkill, WorkExperience, Study, Project
from .serializers import TechnicalSkillCategorySerializer, TechnicalSkillSerializer, WorkExperienceSerializer, \
    StudySerializer, CommentSerializer, ProjectSerializer, MyTokenObtainPairSerializer, UserRegistrationSerializer


class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]


    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ValidateTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'message': 'Token is valid',
            'user': {
                'username': request.user.username,
                'email': request.user.email,
                'is_superuser': request.user.is_superuser
            }
        }, status=status.HTTP_200_OK)


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


class StudyList(ListAPIView):
    queryset = Study.objects.all().order_by('-from_date')
    serializer_class = StudySerializer
    permission_classes = [AllowAny]


class CommentList(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            return Comment.objects.filter(parent=None).order_by('created')
        else:
            return Comment.objects.filter(accepted=True, parent=None).order_by('created')

    def perform_create(self, serializer):
        parent_id = self.request.data.get('parent', None)
        if parent_id is not None:
            try:
                parent = Comment.objects.get(id=parent_id)
                if parent.parent is not None:
                    raise ValidationError('You can only respond to top-level comments.')
            except Comment.DoesNotExist:
                raise ValidationError('Parent comment does not exist.')

        serializer.save()


class ProjectList(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]
