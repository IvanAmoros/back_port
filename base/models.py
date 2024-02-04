from django.db import models


class TechnicalSkillCategory(models.Model):
	name = models.CharField(max_length=100)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


class TechnicalSkill(models.Model):
	category = models.ForeignKey(TechnicalSkillCategory, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name
