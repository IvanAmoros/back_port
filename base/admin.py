from django.contrib import admin

# Register your models here.

from base.models import Comment, TechnicalSkillCategory, TechnicalSkill, WorkExperience, Study, Project, ProjectImage


class TechnicalSkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order_number')
    ordering = ('order_number',)

admin.site.register(TechnicalSkillCategory, TechnicalSkillCategoryAdmin)

admin.site.register(Comment)
admin.site.register(TechnicalSkill)
admin.site.register(WorkExperience)
admin.site.register(Study)
admin.site.register(Project)
admin.site.register(ProjectImage)
