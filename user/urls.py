from django.urls import path
from rest_framework import routers

from user.views import LoginView, UserView

router = routers.SimpleRouter()
router.register('user', UserView)
urlpatterns = [
    path('login/', LoginView.as_view()),
]
