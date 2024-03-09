from django.contrib import admin

# Register your models here.

from base.models import Comment, TechnicalSkillCategory, TechnicalSkill, WorkExperience, Studies

admin.site.register(Comment)
admin.site.register(TechnicalSkillCategory)
admin.site.register(TechnicalSkill)
admin.site.register(WorkExperience)
admin.site.register(Studies)