from django.urls import path
from .views import TechnicalSkillListView


urlpatterns = [
	path('categories/', TechnicalSkillListView.as_view()),
]