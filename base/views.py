from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
import json
from .models import TechnicalSkillCategory, TechnicalSkill, WorkExperience

@method_decorator(csrf_exempt, name='dispatch')
class TechnicalSkillListView(View):
	def get(self, request, *args, **kwargs):
		categories = TechnicalSkillCategory.objects.all()

		categories_with_skills = []
		for category in categories:
			skills = list(category.skills.values('name', 'rating'))
			categories_with_skills.append({
				'category': category.name,
				'skills': skills
			})

		return JsonResponse(categories_with_skills, safe=False)

	@method_decorator(login_required)
	@method_decorator(user_passes_test(lambda u: u.is_superuser))
	def post(self, request, *args, **kwargs):
		data = json.loads(request.body)
		category_name = data.get('category', None)
		skill_name = data.get('name', None)

		if  skill_name:
			if category_name:
				category, created = TechnicalSkillCategory.objects.get_or_create(name=category_name)
			else:
				category_name = None
			skill = TechnicalSkill.objects.create(category=category, name=skill_name)
			return JsonResponse({'message': f'{skill.name} created successfully under category {category.name}'}, status=201)
		else:
			return JsonResponse({'error': 'Name fields are required'}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class WorkExperienceListView(View):
	def get(self, request, *args, **kwargs):
		work_experiences = WorkExperience.objects.all().values()
		return JsonResponse(list(work_experiences), safe=False)
	
	
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


