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
from .serializers import TechnicalSkillCategorySerializer
from rest_framework.generics import ListAPIView


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
 

@method_decorator(csrf_exempt, name='dispatch')
class WorkExperienceListView(APIView):
	@csrf_exempt
	def get(self, request, *args, **kwargs):
		work_experiences = WorkExperience.objects.all().values()
		return JsonResponse(list(work_experiences), safe=False)

	@csrf_exempt
	@permission_classes([IsAdminUser])
	@user_passes_test(lambda u: u.is_superuser)
	def post(self, request, *args, **kwargs):
		data = json.loads(request.body)
		company = data.get('company')
		from_date = data.get('from_date')
		to_date = data.get('to_date')
		current_work = data.get('current_work')
		position = data.get('position')
		job_tasks = data.get('job_tasks', {})
		skills = data.get('skills', [])

		if company and from_date and position:
			work_experience = WorkExperience.objects.create(
				company=company,
				from_date=from_date,
				to_date=to_date,
				current_work=current_work,
				position=position,
				job_tasks=job_tasks
			)

			for skill_data in skills:
				category_name = skill_data.get('category')
				skill_name = skill_data.get('name')

				if skill_name:
					if category_name:
						category, created = TechnicalSkillCategory.objects.get_or_create(name=category_name)
					else:
						category = None

					skill, created = TechnicalSkill.objects.get_or_create(category=category, name=skill_name)
					work_experience.skills.add(skill)
				else:
					return JsonResponse({'error': 'Skill_name field is required'}, status=400)
			return JsonResponse({'message': 'Work experience created successfully'}, status=201)
		else:
			return JsonResponse({'error': 'Company, from_date, and position fields are required'}, status=400)
