from django.urls import path
from .views import TechnicalSkillListView, WorkExperienceListView


urlpatterns = [
	path('skills/', TechnicalSkillListView.as_view()),
	path('works/', WorkExperienceListView.as_view()),
]