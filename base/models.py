from django.db import models


class Comment(models.Model):
	name = models.CharField(max_length=20, blank=True)
	text = models.CharField(max_length=500)
	accepted = models.BooleanField(default=False)
	web_url = models.CharField(max_length=100, blank=True)
	linkedin_url = models.CharField(max_length=100, blank=True)
	github_url = models.CharField(max_length=100, blank=True)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.text


class TechnicalSkillCategory(models.Model):
	name = models.CharField(max_length=100)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


class TechnicalSkill(models.Model):
	name = models.CharField(max_length=100)
	rating = models.FloatField(default=0.0)
	category = models.ForeignKey(
		TechnicalSkillCategory, 
		on_delete=models.CASCADE, 
		related_name='skills',
		null=True,
		blank=True
	)
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
	skills = models.ManyToManyField(TechnicalSkill, blank=True)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.position} at {self.company}"
	

class Studies(models.Model):
	center = models.CharField(max_length=100)
	from_date = models.DateField()
	to_date = models.DateField(null=True, blank=True)
	current = models.BooleanField(default=False)
	tittle = models.CharField(max_length=100)
	description = models.CharField(max_length=200, null=True, blank=True)
	skills = models.ManyToManyField(TechnicalSkill, blank=True)

	def __str__(self):
		return f"{self.tittle} at {self.center}"