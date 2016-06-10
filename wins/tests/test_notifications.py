from django.test import TestCase, Client, override_settings

from ..factories import WinFactory
from ..models import Notification
from alice.tests.client import AliceClient
from users.factories import UserFactory


class NotificationTestCase(TestCase):

    def setUp(self):

        self.client = Client()
        self.alice_client = AliceClient()

        self.user = UserFactory.create()
        self.win = WinFactory.create()

    # GET Schema --------------------------------------------------------------

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_post_pass(self):

        response = self.alice_client.post("/notifications/", {
            "win": str(self.win.pk),
            "user": self.user.pk,
            "recipient": "root@nowhere.ca",
            "type": Notification.TYPE_OFFICER
        })

        self.assertEqual(response.status_code, 201)
