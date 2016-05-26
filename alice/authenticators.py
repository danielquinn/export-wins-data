import logging

from hashlib import sha256

from django.conf import settings

from rest_framework.permissions import IsAuthenticated, AllowAny


class SignatureMixin(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def _test_signature(self, request):

        offered = request.META.get("HTTP_X_SIGNATURE")

        if not offered:
            return False

        salt = bytes(settings.UI_SECRET, "utf-8")
        path = bytes(request.get_full_path(), "utf-8")
        body = request.body
        generated = sha256(path + body + salt).hexdigest()

        self.logger.debug("  {} vs. {}".format(generated, offered))

        return self._strings_match(generated, offered)

    @staticmethod
    def _strings_match(a, b):
        """
        Constant time string comparison, mitigates side channel attacks.
        See: https://github.com/kumar303/mohawk/blob/master/mohawk/util.py#L196
        """

        if len(a) != len(b):
            return False

        result = 0

        def byte_ints(buffer):
            for character in buffer:
                # In Python 3, if we have a bytes object, iterating it will
                # already get the integer value. In older pythons, we need
                # to use ord().
                if not isinstance(character, int):
                    character = ord(character)
                yield character

        for x, y in zip(byte_ints(a), byte_ints(b)):
            result |= x ^ y

        return result == 0


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
