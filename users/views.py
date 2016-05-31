from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import LoggingAuthTokenSerializer


class LoggingObtainAuthToken(ObtainAuthToken):
    serializer_class = LoggingAuthTokenSerializer
