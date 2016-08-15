from django.contrib.auth import login
from rest_framework import parsers, renderers
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoggingAuthTokenSerializer


class LoginView(APIView):

    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = LoggingAuthTokenSerializer
    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        login(request, user)

        return Response({'id': user.pk, 'email': user.email})
