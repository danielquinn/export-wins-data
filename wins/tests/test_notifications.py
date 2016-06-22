from django.core import mail
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

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_officer_intermediate_email(self):
        # for now, when asking for officer email, should send the intemediate one

        response = self.alice_client.post("/notifications/", {
            "win": str(self.win.pk),
            "user": self.user.pk,
            "type": Notification.TYPE_OFFICER
        })

        self.assertEqual(response.status_code, 201)
        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, 'Thank you for submitting a new Export Win.')
        self.assertIn(
            'there may be a delay before we contact Customers to confirm Export Wins',
            mail.outbox[0].body,
        )

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_customer_email_not_sent(self):

        response = self.alice_client.post("/notifications/", {
            "win": str(self.win.pk),
            "user": self.user.pk,
            "type": Notification.TYPE_CUSTOMER
        })

        self.assertEqual(response.status_code, 201)
        self.assertEquals(len(mail.outbox), 0)