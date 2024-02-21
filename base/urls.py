from django.urls import path
from .views import TechnicalSkillCategoryList, WorkExperienceListView, ValidateTokenView
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
	path('skills/', TechnicalSkillCategoryList.as_view()),
	path('works/', WorkExperienceListView.as_view()),
	path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('api/validate_token/', ValidateTokenView.as_view(), name='validate_token'),
	# path('login/', LoginAPIView.as_view()),
	# path('logout/', LogoutAPIView.as_view()),
]