from django.db import models
import json


class TechnicalSkillCategory(models.Model):
	name = models.CharField(max_length=100)
	skills = models.ManyToManyField('TechnicalSkill', related_name='skill_categories')
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


class TechnicalSkill(models.Model):
	categories = models.ManyToManyField(TechnicalSkillCategory, related_name='skill_skills', blank=True)
	name = models.CharField(max_length=100)
	rating = models.FloatField(default=0.0)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name
	

class WorkExperience(models.Model):
	company = models.CharField(max_length=100)
	from_date = models.DateField()
	to_date = models.DateField(null=True, blank=True)
	current_work = models.BooleanField(default=False)
	position = models.CharField(max_length=100)
	job_tasks = models.JSONField()
	skills = models.ManyToManyField(TechnicalSkill)

	def __str__(self):
		return f"{self.position} at {self.company}"

	def set_job_tasks(self, tasks):
		self.job_tasks = json.dumps(tasks)

	def get_job_tasks(self):
		return json.loads(self.job_tasks)

