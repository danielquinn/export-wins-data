from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from .models import Win, Breakdown, Advisor, CustomerResponse
from .serializers import (
    WinSerializer, BreakdownSerializer, AdvisorSerializer, 
    CustomerResponseSerializer
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
