from rest_framework import filters
from rest_framework.decorators import list_route
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from alice.authenticators import SignatureOnlyAlicePermission

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


class LimitedWinViewSet(WinViewSet):

    serializer_class = LimitedWinSerializer
    permission_classes = (SignatureOnlyAlicePermission,)
    http_method_names = ("get",)

    def get_queryset(self):

        # We only allow for specific wins to be queried here
        if "pk" not in self.kwargs:
            return WinViewSet.get_queryset(self).none()

        # Limit records to wins that have not already been confirmed
        return WinViewSet.get_queryset(self).filter(
            pk=self.kwargs["pk"],
            confirmation__isnull=True
        )


class NotificationViewSet(ModelViewSet):

    model = Notification
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (SignatureOnlyAlicePermission,)
    pagination_class = StandardPagination
    http_method_names = ("post",)

    def perform_create(self, serializer):
        instance = serializer.save()
        if instance.type == Notification.TYPE_OFFICER:
            serializer.send_officer_email(instance)
        elif instance.type == Notification.TYPE_CUSTOMER:
            serializer.send_customer_email(self.request, instance)
        return instance


class ConfirmationViewSet(ModelViewSet):

    model = CustomerResponse
    queryset = CustomerResponse.objects.all()
    serializer_class = CustomerResponseSerializer
    pagination_class = StandardPagination
    permission_classes = (SignatureOnlyAlicePermission,)
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ("pk",)
    http_method_names = ("get", "post")

    @list_route(methods=("get",))
    def schema(self, request):
        return Response(
            self.metadata_class().get_serializer_info(self.get_serializer()))


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
