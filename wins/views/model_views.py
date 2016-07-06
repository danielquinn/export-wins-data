from rest_framework.decorators import list_route
from rest_framework.filters import DjangoFilterBackend, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .. import notifications
from ..filters import CustomerResponseFilterSet
from ..models import Win, Breakdown, Advisor, CustomerResponse, Notification
from ..serializers import (
    WinSerializer, LimitedWinSerializer, BreakdownSerializer,
    AdvisorSerializer, CustomerResponseSerializer, NotificationSerializer
)
from alice.views import AliceMixin


class StandardPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page-size"


class BigPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = "page-size"


class WinViewSet(AliceMixin, ModelViewSet):

    model = Win
    queryset = Win.objects.all()
    serializer_class = WinSerializer
    pagination_class = BigPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('id', 'user__id')
    ordering_fields = ("pk",)
    http_method_names = ("get", "post", "put")


class LimitedWinViewSet(WinViewSet):

    serializer_class = LimitedWinSerializer
    permission_classes = (AllowAny,)
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
    """ Endpoint to instruct data server to notify officer or customer """

    model = Notification
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (AllowAny,)
    pagination_class = StandardPagination
    http_method_names = ("post",)

    def perform_create(self, serializer):
        instance = serializer.save()
        if instance.type == Notification.TYPE_OFFICER:
            notifications.send_intermediate_officer_email(instance.win)
        # elif instance.type == Notification.TYPE_CUSTOMER:
        #     notifications.send_customer_email(self.request, instance.win)
        return instance


class ConfirmationViewSet(ModelViewSet):

    model = CustomerResponse
    queryset = CustomerResponse.objects.all()
    serializer_class = CustomerResponseSerializer
    pagination_class = StandardPagination
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = CustomerResponseFilterSet
    ordering_fields = ("pk",)
    http_method_names = ("get", "post")

    @list_route(methods=("get",))
    def schema(self, request):
        return Response(
            self.metadata_class().get_serializer_info(self.get_serializer()))

    def perform_create(self, serializer):
        instance = serializer.save()
        notifications.send_officer_notification_of_customer_response(instance)
        return instance


class BreakdownViewSet(AliceMixin, ModelViewSet):

    model = Breakdown
    queryset = Breakdown.objects.all()
    serializer_class = BreakdownSerializer
    pagination_class = StandardPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ("pk",)
    http_method_names = ("get", "post")


class AdvisorViewSet(AliceMixin, ModelViewSet):

    model = Advisor
    queryset = Advisor.objects.all()
    serializer_class = AdvisorSerializer
    pagination_class = StandardPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ("pk",)
    http_method_names = ("get", "post")
