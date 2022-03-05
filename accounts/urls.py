from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from accounts.views import CustomUserCreate, CheckDuplicatedId, ReturnId

app_name = 'users'

urlpatterns = [
    path('register/', CustomUserCreate.as_view(), name="create_user"),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('checkid/', CheckDuplicatedId.as_view(), name='check_duplicated_id'),
    path('returnid/', ReturnId.as_view(), name='return_id')

]