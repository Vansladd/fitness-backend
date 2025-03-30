from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StepRecordViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CustomTokenObtainPairView, RegisterView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r"steps", StepRecordViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/register/", RegisterView.as_view(), name="register"),
]