from django.urls import path
from user import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    # 회원가입, 로그인, 리프레쉬 토큰 순
    path('signup/', views.SignupView.as_view(), name='sign_up_view'), # /users/signup/
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 프로필, 팔로우 순
    path('profile/<int:user_id>/', views.ProfileView.as_view(), name="profile_view"), # /users/profile/<int:user_id>/
]
