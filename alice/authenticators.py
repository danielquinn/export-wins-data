import logging

from hashlib import sha256

from django.conf import settings

from rest_framework.permissions import IsAuthenticated


class AlicePermission(IsAuthenticated):

    def __init__(self):
        IsAuthenticated.__init__(self)
        self.logger = logging.getLogger(__name__)

    def has_permission(self, request, view):

        self.logger.debug(
            "{} to {}".format(request.method, request.get_full_path()))

        if view.action == "schema":
            if self._test_signature(request):
                self.logger.debug("OK: schema & signature")
                return True

        if not IsAuthenticated.has_permission(self, request, view):
            self.logger.debug("Not authenticated: {}".format(
                request.META.get("Authorization")))
            return False

        if self._test_signature(request):
            self.logger.debug("OK: signature")
            return True

        self.logger.debug("Bad signature")

        return False

    def _test_signature(self, request):

        offered = request.META.get("HTTP_X_SIGNATURE")
        salt = bytes(settings.UI_SECRET, "utf-8")
        path = bytes(request.get_full_path(), "utf-8")
        body = request.body
        generated = sha256(path + body + salt).hexdigest()

        self.logger.debug("{} vs. {}".format(generated, offered))

        return generated == offered
