from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from users.views import LoginView
from wins.views import (
    WinViewSet, BreakdownViewSet, AdvisorViewSet, ConfirmationViewSet,
    NotificationViewSet, LimitedWinViewSet
)

router = DefaultRouter()
router.register(r"wins", WinViewSet)
router.register(r"limited-wins", LimitedWinViewSet, base_name="limited-win")
router.register(r"confirmations", ConfirmationViewSet)
router.register(r"breakdowns", BreakdownViewSet)
router.register(r"advisors", AdvisorViewSet)
router.register(r"notifications", NotificationViewSet)

urlpatterns = [

    url(r"^", include(router.urls, namespace="drf")),

    # Override DRF's default 'cause our includes brute-force protection
    url(r"^auth/login/$", LoginView.as_view(), name="login"),

    url(r"^auth/", include('rest_framework.urls', namespace="rest_framework")),

]
