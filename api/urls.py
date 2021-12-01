from django.urls import path, include
from . import views
from .views import *
from rest_framework import routers
from rest_framework_jwt.views import verify_jwt_token
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
