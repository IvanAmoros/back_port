from django.urls import path
from .views import TechnicalSkillCategoryList, WorkExperienceList, ValidateTokenView, TechnicalSkillCategoryCreate, TechnicalSkillCreate, TechnicalSkillUpdate, TechnicalSkillCategoryUpdate
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
	path('skills/', TechnicalSkillCategoryList.as_view()),
	path('categories/create/', TechnicalSkillCategoryCreate.as_view(), name='category-create'),
    path('skills/create/', TechnicalSkillCreate.as_view(), name='skill-create'),
	path('skills/<int:pk>/', TechnicalSkillUpdate.as_view(), name='technical-skill-update'),
    path('categories/<int:pk>/', TechnicalSkillCategoryUpdate.as_view(), name='technical-skill-category-update'),

	path('works/', WorkExperienceList.as_view()),

	path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('api/validate_token/', ValidateTokenView.as_view(), name='validate_token'),
	# path('login/', LoginAPIView.as_view()),
	# path('logout/', LogoutAPIView.as_view()),
]