from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from .models import Win, Breakdown, Advisor, CustomerResponse, Notification
from .serializers import (
    WinSerializer, LimitedWinSerializer, BreakdownSerializer,
    AdvisorSerializer, CustomerResponseSerializer, NotificationSerializer
)

from alice.views import AliceMixin


class StandardPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page-size"
    max_page_size = 100000


class WinViewSet(AliceMixin, ModelViewSet):

    model = Win
    queryset = Win.objects.all()
    serializer_class = WinSerializer
    pagination_class = StandardPagination
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ("pk",)
    http_method_names = ("get", "post")


class LimitedViewSet(WinViewSet):

    serializer_class = LimitedWinSerializer
    permission_classes = (AllowAny,)
    http_method_names = ("get",)

    def get_queryset(self):
        return WinViewSet.get_queryset(self).filter(confirmation__isnull=True)


class NotificationViewSet(AliceMixin, ModelViewSet):

    model = Notification
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (AllowAny,)
    pagination_class = StandardPagination
    http_method_names = ("post",)

    def perform_create(self, serializer):
        instance = serializer.save()
        serializer.send_officer_email(instance)
        serializer.send_customer_email(self.request, instance)
        return instance


class ConfirmationViewSet(AliceMixin, ModelViewSet):

    model = CustomerResponse
    queryset = CustomerResponse.objects.all()
    serializer_class = CustomerResponseSerializer
    pagination_class = StandardPagination
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ("pk",)
    http_method_names = ("get", "post")


class BreakdownViewSet(AliceMixin, ModelViewSet):

    model = Breakdown
    queryset = Breakdown.objects.all()
    serializer_class = BreakdownSerializer
    pagination_class = StandardPagination
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ("pk",)
    http_method_names = ("get", "post")


class AdvisorViewSet(AliceMixin, ModelViewSet):

    model = Advisor
    queryset = Advisor.objects.all()
    serializer_class = AdvisorSerializer
    pagination_class = StandardPagination
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ("pk",)
    http_method_names = ("get", "post")
