from rest_framework.authentication import SessionAuthentication


class NoCSRFSessionAuthentication(SessionAuthentication):
    """
    This is only here because we're guaranteeing the communications between the
    UI server and the data server to be legit on account of the request signing
    in Alice.

    We're abusing DRF's SessionAuthentication here, which is typically used to
    auth local requests on the server (for javascript and the BrowseableAPI).
    Instead, we're spoofing the login session id via alice.rabbit on the ui,
    and don't want to worry about csrf protection on the data server.  That's
    why we'r effectively ignoring it for this case.

    If you ever decide to open the data server, you're going to have to modify
    the UI server to implement Oauth to do things properly.  Have fun with
    that ;-)
    """

    def enforce_csrf(self, request):
        pass
