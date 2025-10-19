from django.urls import path
from rest_framework import routers

from user.views import LoginView, UserView, UserBalanceViewSet, BalanceHistoryViewSet

router = routers.SimpleRouter()
router.register('user', UserView)
router.register('user_balance', UserBalanceViewSet)
router.register('user_balance_history', BalanceHistoryViewSet)
urlpatterns = [
    path('login/', LoginView.as_view()),
]
