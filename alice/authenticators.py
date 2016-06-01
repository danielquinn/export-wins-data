import logging

from rest_framework.permissions import IsAuthenticated, SAFE_METHODS


class AlicePermission(IsAuthenticated):
    """
    Allows a GET request to schema, and view-defined requests to everything
    else so long as they're authenticated.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        IsAuthenticated.__init__(self)

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            if view.action == "schema":
                self.logger.debug("OK: schema & signature")
                return True

        if IsAuthenticated.has_permission(self, request, view):
            return True

        self.logger.debug("Not authenticated: {}".format(
            request.META.get("Authorization")))

        return False
