from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.exceptions import ValidationError

from .models import Comment, TechnicalSkillCategory, TechnicalSkill, WorkExperience, Study, Project
from .serializers import TechnicalSkillCategorySerializer, TechnicalSkillSerializer, WorkExperienceSerializer, \
    StudySerializer, CommentSerializer, ProjectSerializer



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs) -> dict[str, str]:
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['is_superuser'] = self.user.is_superuser
        return data


def get(request):
    try:
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
        })
    except Exception as e:
        return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ValidateTokenView(APIView):
    permission_classes = (permissions.IsAuthenticated,)


class TechnicalSkillCategoryList(ListAPIView):
    queryset = TechnicalSkillCategory.objects.all().order_by('order_number')
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
