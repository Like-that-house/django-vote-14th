from django.urls import path, include
from . import views
from .views import *
from rest_framework import routers
from rest_framework_jwt.views import verify_jwt_token
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'candidates', CandidateViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('users/login', views.LoginView.as_view()),
    path('users/vote/<int:id>', views.VoteView.as_view()),
    path('token', obtain_jwt_token),
    path('users/token/refresh', refresh_jwt_token),
    path('users/token/verify', verify_jwt_token),
]