from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
import json
from .models import TechnicalSkillCategory, TechnicalSkill

@method_decorator(csrf_exempt, name='dispatch')
class TechnicalSkillListView(View):
	def get(self, request, *args, **kwargs):
		skills = list(TechnicalSkill.objects.values())
		return JsonResponse({'skills': skills})

	@method_decorator(login_required)  # Ensure the user is logged in
	@method_decorator(user_passes_test(lambda u: u.is_superuser))  # Ensure the user is a superuser
	def post(self, request, *args, **kwargs):
		data = json.loads(request.body)
		category_name = data.get('category', None)
		skill_name = data.get('name', None)

		if category_name and skill_name:
			category, created = TechnicalSkillCategory.objects.get_or_create(name=category_name)
			skill = TechnicalSkill.objects.create(category=category, name=skill_name)
			return JsonResponse({'message': f'{skill.name} created successfully under category {category.name}'}, status=201)
		else:
			return JsonResponse({'error': 'Both category and name fields are required'}, status=400)
