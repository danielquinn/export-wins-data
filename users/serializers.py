from datetime import datetime
from dateutil.relativedelta import relativedelta

from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import serializers

from .models import LoginFailure


class LoggingAuthTokenSerializer(AuthTokenSerializer):

    WINDOW = 5  # Minutes of wait time before we allow attempts again
    STRIKES = 3  # Number of failed logins before we complain

    def validate(self, attrs):

        email = attrs.get("username")
        window_start = datetime.utcnow() - relativedelta(minutes=self.WINDOW)

        failures = LoginFailure.objects.filter(
            email=email, created__gt=window_start).count()

        if failures >= self.STRIKES:
            raise serializers.ValidationError(
                "Too many failed logins.  Please wait at least {} minutes and "
                "try again.".format(self.WINDOW)
            )

        try:
            return AuthTokenSerializer.validate(self, attrs)
        except Exception as e:
            LoginFailure.objects.create(email=email)
            raise e
