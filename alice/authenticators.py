import logging

from hashlib import sha256

from django.conf import settings
from django.utils.crypto import constant_time_compare

from rest_framework.permissions import IsAuthenticated, AllowAny


class SignatureMixin(object):
    """
    Mixin providing the `_test_signature` method for authenticating that the
    request is from a trusted client
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def _generate_signature(self, secret, path, body):
        salt = bytes(secret, "utf-8")
        path = bytes(path, "utf-8")
        return sha256(path + body + salt).hexdigest()

    def _test_signature(self, request):
        """
        Has client provided valid request signature, signed with secret key?
        """

        offered = request.META.get("HTTP_X_SIGNATURE")

        if not offered:
            return False

        generated = self._generate_signature(
            settings.UI_SECRET,
            request.get_full_path(),
            request.body,
        )
        self.logger.debug("  {} vs. {}".format(generated, offered))

        return constant_time_compare(generated, offered)


class AlicePermission(SignatureMixin, IsAuthenticated):
    """
    Makes sure that the request is both authorised with a server key as well as
    a user token.
    """

    def __init__(self):
        SignatureMixin.__init__(self)
        IsAuthenticated.__init__(self)

    def has_permission(self, request, view):

        if view.action == "schema":
            if self._test_signature(request):
                self.logger.debug("  OK: schema & signature")
                return True
            self.logger.debug("  Bad signature")
            return False

        if not IsAuthenticated.has_permission(self, request, view):
            self.logger.debug("  Not authenticated: {}".format(
                request.META.get("Authorization")))
            return False

        if self._test_signature(request):
            self.logger.debug("  OK: signature")
            return True

        self.logger.debug("  Bad signature")

        return False


class SignatureOnlyAlicePermission(SignatureMixin, AllowAny):
    """
    Use this for services that must be available to a client with a server key
    but where we don't have any user data (or have no use for it).
    """

    def __init__(self):
        SignatureMixin.__init__(self)
        AllowAny.__init__(self)

    def has_object_permission(self, request, view, obj):
        return self._test_signature(request)

    def has_permission(self, request, view):
        return self._test_signature(request)
