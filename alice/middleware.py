import logging

from hashlib import sha256

from django.conf import settings
from django.http import HttpResponseBadRequest


class SignatureRejectionMiddleware:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def process_request(self, request):
        if not self._test_signature(request):
            return HttpResponseBadRequest("PFO")

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
