from django.contrib import admin

# Register your models here.

from base.models import TechnicalSkillCategory, TechnicalSkill, WorkExperience

admin.site.register(TechnicalSkillCategory)
admin.site.register(TechnicalSkill)
admin.site.register(WorkExperience)