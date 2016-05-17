from hashlib import sha256

from django.conf import settings

from rest_framework.permissions import IsAuthenticated


class AlicePermission(IsAuthenticated):

    def has_permission(self, request, view):
        print(request.method, request.get_full_path(), end=" ")
        if view.action == "schema":
            if self._test_signature(request):
                print("OK: schema & signature")
                return True

        if not IsAuthenticated.has_permission(self, request, view):
            print("Not authenticated: {}".format(request.META.get("Authorization")))
            return False

        if self._test_signature(request):
            print("OK: signature")
            return True
        print("Bad signature")
        return False

    @staticmethod
    def _test_signature(request):

        offered = request.META.get("HTTP_X_SIGNATURE")
        salt = bytes(settings.UI_SECRET, "utf-8")
        path = bytes(request.get_full_path(), "utf-8")
        body = request.body
        generated = sha256(path + body + salt).hexdigest()
        print(generated, "vs.", offered)
        return generated == offered
