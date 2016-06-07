import json

from django.test import TestCase, Client, override_settings
from django.core.urlresolvers import reverse
from rest_framework.authtoken.models import Token

from ..factories import WinFactory
from ..models import Breakdown, Notification
from alice.tests.client import AliceClient
from users.factories import UserFactory


class AlicePermissionTestCase(TestCase):

    def setUp(self):

        self.client = Client()
        self.alice_client = AliceClient()

        self.user = UserFactory.create()
        self.user.set_password('asdf')
        self.user.save()

        self.superuser = UserFactory.create(is_superuser=True, email="a@b.c")

        self.wins_schema = reverse("drf:win-schema")
        self.wins_list = reverse("drf:win-list")
        self.wins_detail = reverse("drf:win-detail", kwargs={
            "pk": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        })
        self.notifications_list = reverse("drf:notification-list")
        self.notifications_detail = reverse("drf:notification-detail", kwargs={
            "pk": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        })
        self.customerresponses_schema = reverse("drf:customerresponse-schema")
        self.customerresponses_list = reverse("drf:customerresponse-list")
        self.customerresponses_detail = reverse("drf:customerresponse-detail", kwargs={
            "pk": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        })
        self.breakdowns_schema = reverse("drf:breakdown-schema")
        self.breakdowns_list = reverse("drf:breakdown-list")
        self.breakdowns_detail = reverse("drf:breakdown-detail", kwargs={
            "pk": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        })
        self.advisors_schema = reverse("drf:advisor-schema")
        self.advisors_list = reverse("drf:advisor-list")
        self.advisors_detail = reverse("drf:advisor-detail", kwargs={
            "pk": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        })

        self.win = WinFactory.create()

        self.WINS_POST_SAMPLE = {
          "user": 1,
          "cdms_reference": "cdms reference",
          "company_name": "company name",
          "country": "AF",
          "created": "2016-05-17T12:44:48.021705Z",
          "customer_email_address": "no@way.ca",
          "customer_job_title": "customer job title",
          "customer_location": 3,
          "customer_name": "customer name",
          "date": "1979-06-01",
          "description": "asdlkjskdlfkjlsdjkl",
          "goods_vs_services": 1,
          "has_hvo_specialist_involvement": True,
          "hq_team": "other:1",
          "hvo_programme": "BSC-01",
          "is_e_exported": True,
          "is_line_manager_confirmed": True,
          "is_personally_confirmed": True,
          "is_prosperity_fund_related": True,
          "lead_officer_name": "lead officer name",
          "line_manager_name": "line manager name",
          "location": "Edinburgh, UK",
          "sector": 1,
          "team_type": "investment",
          "total_expected_export_value": 5,
          "total_expected_non_export_value": 5,
          "type": 1,
          "type_of_support_1": 1,
        }

        self.NOTIFICATIONS_POST_SAMPLE = {
            "win": str(self.win.pk),
            "user": self.user.pk,
            "recipient": "root@nowhere.ca",
            "type": Notification.TYPE_OFFICER
        }

        self.CUSTOMER_RESPONSES_POST_SAMPLE = {
            "win": str(self.win.pk),
            "name": "bob",
            "improved_profile": "1",
            "gained_confidence": "1",
            "access_to_information": "1",
            "expected_portion_without_help": "1",
            "last_export": "1",
            "overcame_problem": "1",
            "developed_relationships": "1",
            "access_to_contacts": "1",
        }

        self.BREAKDOWNS_POST_SAMPLE = {
            "win": str(self.win.pk),
            "type": Breakdown.TYPE_EXPORT,
            "year": "1999",
            "value": "1",
        }

        self.ADVISORS_POST_SAMPLE = {
            "name": "bob",
            "team_type": "other",
            "hq_team": "team:1",
            "location": "france"
        }

    # GET Schema --------------------------------------------------------------

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_get_notification_schema_not_allowed(self):
        response = self.alice_client.get('/notification/schema/')
        self.assertEqual(response.status_code, 404)

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def _test_get_schema_pass(self, url, keys):
        response = self.alice_client.get(url)
        content = json.loads(str(response.content, "utf-8"))
        self.assertEqual(response.status_code, 200)
        for key in keys:
            self.assertIn(key, content)

    def test_win_schema_pass(self):
        self._test_get_schema_pass(
            self.wins_schema,
            ['id', 'user', 'company_name', 'cdms_reference', 'cdms_reference'],
        )

    def test_customerresponse_schema_pass(self):
        self._test_get_schema_pass(
            self.customerresponses_schema,
            ['access_to_contacts', 'access_to_information'],
        )

    def test_breakdown_schema_pass(self):
        self._test_get_schema_pass(
            self.breakdowns_schema,
            ['win', 'type', 'year', 'value'],
        )

    def test_advisor_schema_pass(self):
        self._test_get_schema_pass(
            self.advisors_schema,
            ['name', 'team_type', 'hq_team', 'location'],
        )

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def _test_get_schema_fail_bad_client(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_win_schema_fail_bad_client(self):
        self._test_get_schema_fail_bad_client(self.wins_schema)

    def test_customerresponse_schema_fail_bad_client(self):
        self._test_get_schema_fail_bad_client(self.customerresponses_schema)

    def test_breakdown_schema_fail_bad_client(self):
        self._test_get_schema_fail_bad_client(self.breakdowns_schema)

    def test_advisor_schema_fail_bad_client(self):
        self._test_get_schema_fail_bad_client(self.advisors_schema)

    # GET List ----------------------------------------------------------------

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_get_notification_list_not_allowed(self):
        self._login(signed=True)
        response = self.alice_client.get(self.notifications_list)
        self.assertEqual(response.status_code, 405)

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def _test_get_list_pass(self, url):
        self._login(signed=True)
        response = self.alice_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_wins_get_list_pass(self):
        self._test_get_list_pass(self.wins_list)

    def test_customerresponse_get_list_pass(self):
        self._test_get_list_pass(self.customerresponses_list)

    def test_breakdowns_get_list_pass(self):
        self._test_get_list_pass(self.breakdowns_list)

    def test_advisors_get_list_pass(self):
        self._test_get_list_pass(self.advisors_list)

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def _test_get_list_fail_no_auth(self, url):
        response = self.alice_client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_wins_get_list_fail_no_auth(self):
        self._test_get_list_fail_no_auth(self.wins_list)

    def test_breakdowns_get_list_fail_no_auth(self):
        self._test_get_list_fail_no_auth(self.breakdowns_list)

    def test_advisors_get_list_fail_no_auth(self):
        self._test_get_list_fail_no_auth(self.advisors_list)

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def _test_get_list_fail_no_signature(self, url):
        self._login()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_wins_get_list_fail_no_signature(self):
        self._test_get_list_fail_no_signature(self.wins_list)

    def test_customerresponses_get_list_fail_no_signature(self):
        self._test_get_list_fail_no_signature(self.customerresponses_list)

    def test_breakdowns_get_list_fail_no_signature(self):
        self._test_get_list_fail_no_signature(self.breakdowns_list)

    def test_advisors_get_list_fail_no_signature(self):
        self._test_get_list_fail_no_signature(self.advisors_list)

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def _test_get_list_fail_bad_signature(self, url):
        auth = {
            "HTTP_X_SIGNATURE": "bad-signature",
        }
        self._login(signed=True)
        response = self.alice_client.get(url, **auth)
        self.assertEqual(response.status_code, 400)

    def test_wins_get_list_fail_bad_signature(self):
        self._test_get_list_fail_bad_signature(self.wins_list)

    def test_customerresponses_get_list_fail_bad_signature(self):
        self._test_get_list_fail_bad_signature(self.customerresponses_list)

    def test_breakdowns_get_list_fail_bad_signature(self):
        self._test_get_list_fail_bad_signature(self.breakdowns_list)

    def test_advisors_get_list_fail_bad_signature(self):
        self._test_get_list_fail_bad_signature(self.advisors_list)

    # GET Detail --------------------------------------------------------------

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_get_notification_detail_not_allowed(self):
        self._login(signed=True)
        response = self.alice_client.get(self.notifications_detail)
        self.assertEqual(response.status_code, 405)

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def _test_get_detail_pass(self, url):
        self._login(signed=True)
        response = self.alice_client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_wins_get_detail_pass(self):
        self._test_get_detail_pass(self.wins_detail)

    def test_customerresponses_get_detail_pass(self):
        self._test_get_detail_pass(self.customerresponses_detail)

    def test_breakdowns_get_detail_pass(self):
        self._test_get_detail_pass(self.breakdowns_detail)

    def test_advisors_get_detail_pass(self):
        self._test_get_detail_pass(self.advisors_detail)

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def _test_get_detail_fail_no_auth(self, url):
        response = self.alice_client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_wins_get_detail_fail_no_auth(self):
        self._test_get_detail_fail_no_auth(self.wins_detail)

    def test_breakdowns_get_detail_fail_no_auth(self):
        self._test_get_detail_fail_no_auth(self.breakdowns_detail)

    def test_advisors_get_detail_fail_no_auth(self):
        self._test_get_detail_pass(self.advisors_detail)

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def _test_get_detail_fail_no_signature(self, url):
        self._login()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_wins_get_detail_fail_no_signature(self):
        self._test_get_detail_fail_no_signature(self.wins_detail)

    def test_customerresponses_get_detail_fail_no_signature(self):
        self._test_get_detail_fail_no_signature(self.customerresponses_detail)

    def test_breakdowns_get_detail_fail_no_signature(self):
        self._test_get_detail_fail_no_signature(self.breakdowns_detail)

    def test_advisors_get_detail_fail_no_signature(self):
        self._test_get_detail_fail_no_signature(self.advisors_detail)

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def _test_get_detail_fail_bad_signature(self, url):
        auth = {
            "HTTP_X_SIGNATURE": "bad-signature",
        }
        self._login(signed=True)
        response = self.alice_client.get(url, **auth)
        self.assertEqual(response.status_code, 400)

    def test_wins_get_detail_fail_bad_signature(self):
        self._test_get_detail_fail_bad_signature(self.wins_detail)

    def test_customerresponses_get_detail_fail_bad_signature(self):
        self._test_get_detail_fail_bad_signature(self.customerresponses_detail)

    def test_breakdowns_get_detail_fail_bad_signature(self):
        self._test_get_detail_fail_bad_signature(self.breakdowns_detail)

    def test_advisors_get_detail_fail_bad_signature(self):
        self._test_get_detail_pass(self.advisors_detail)

    # POST --------------------------------------------------------------------

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def _test_post_pass(self, url, data):
        self._login(signed=True)
        response = self.alice_client.post(url, data)
        self.assertEqual(response.status_code, 201, response.content)

    def test_wins_post_pass(self):
        self._test_post_pass(self.wins_list, self.WINS_POST_SAMPLE)

    def test_notifications_post_pass(self):
        self._test_post_pass(
            self.notifications_list,
            self.NOTIFICATIONS_POST_SAMPLE,
        )

    def test_customerresponses_post_pass(self):
        self._test_post_pass(
            self.customerresponses_list,
            self.CUSTOMER_RESPONSES_POST_SAMPLE,
        )

    def test_breakdowns_post_pass(self):
        self._test_post_pass(
            self.breakdowns_list,
            self.BREAKDOWNS_POST_SAMPLE,
        )

    def test_advisors_post_pass(self):
        self._test_post_pass(
            self.advisors_list,
            self.ADVISORS_POST_SAMPLE,
        )

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def _test_post_fail_no_auth(self, url, data):
        response = self.alice_client.post(url, data)
        self.assertEqual(response.status_code, 403)

    def test_wins_post_fail_no_auth(self):
        self._test_post_fail_no_auth(self.wins_list, self.WINS_POST_SAMPLE)

    def test_breakdowns_post_fail_no_auth(self):
        self._test_post_fail_no_auth(
            self.breakdowns_list,
            self.BREAKDOWNS_POST_SAMPLE,
        )

    def test_advisors_post_fail_no_auth(self):
        self._test_post_fail_no_auth(
            self.advisors_list,
            self.ADVISORS_POST_SAMPLE,
        )

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def _test_post_fail_bad_auth(self, url, data):
        self.alice_client.login(username="not-a-user", password="fail")
        response = self.alice_client.post(url, data)
        self.assertEqual(response.status_code, 403)

    def test_wins_post_fail_bad_auth(self):
        self._test_post_fail_bad_auth(
            self.wins_list,
            self.WINS_POST_SAMPLE,
        )

    def test_breakdowns_post_fail_bad_auth(self):
        self._test_post_fail_bad_auth(
            self.breakdowns_list,
            self.BREAKDOWNS_POST_SAMPLE,
        )

    def test_advisors_post_fail_bad_auth(self):
        self._test_post_fail_bad_auth(
            self.advisors_list,
            self.ADVISORS_POST_SAMPLE,
        )

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def _test_post_fail_no_signature(self, url, data):
        self._login()
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_wins_post_fail_no_signature(self):
        self._test_post_fail_no_signature(
            self.wins_list,
            self.WINS_POST_SAMPLE,
        )

    def test_notifications_post_fail_no_signature(self):
        self._test_post_fail_no_signature(
            self.notifications_list,
            self.NOTIFICATIONS_POST_SAMPLE,
        )

    def test_customerresponses_post_fail_no_signature(self):
        self._test_post_fail_no_signature(
            self.customerresponses_list,
            self.CUSTOMER_RESPONSES_POST_SAMPLE,
        )

    def test_breakdowns_post_fail_no_signature(self):
        self._test_post_fail_no_signature(
            self.breakdowns_list,
            self.BREAKDOWNS_POST_SAMPLE,
        )

    def test_advisors_post_fail_no_signature(self):
        self._test_post_fail_no_signature(
            self.advisors_list,
            self.ADVISORS_POST_SAMPLE,
        )

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def _test_post_fail_bad_signature(self, url, data):
        auth = {
            "HTTP_X_SIGNATURE": "bad-signature"
        }
        self._login(signed=True)
        response = self.alice_client.post(url, data, **auth)
        self.assertEqual(response.status_code, 400)

    def test_wins_post_fail_bad_signature(self):
        self._test_post_fail_bad_signature(
            self.wins_list,
            self.WINS_POST_SAMPLE,
        )

    def test_notifications_post_fail_bad_signature(self):
        self._test_post_fail_bad_signature(
            self.notifications_list,
            self.NOTIFICATIONS_POST_SAMPLE,
        )

    def test_customerresponses_post_fail_bad_signature(self):
        self._test_post_fail_bad_signature(
            self.customerresponses_list,
            self.CUSTOMER_RESPONSES_POST_SAMPLE,
        )

    def test_breakdowns_post_fail_bad_signature(self):
        self._test_post_fail_bad_signature(
            self.breakdowns_list,
            self.BREAKDOWNS_POST_SAMPLE,
        )

    def test_advisors_post_fail_bad_signature(self):
        self._test_post_fail_bad_signature(
            self.advisors_list,
            self.ADVISORS_POST_SAMPLE,
        )

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def _test_post_fail_no_data(self, url, data, key):
        self._login(signed=True)
        response = self.alice_client.post(url, {})
        self.assertEqual(response.status_code, 400)
        content = json.loads(str(response.content, "utf-8"))
        self.assertIn(key, content)
        self.assertEqual(content[key], ["This field is required."])

    def test_wins_post_fail_no_data(self):
        self._test_post_fail_no_data(
            self.wins_list,
            self.WINS_POST_SAMPLE,
            'customer_email_address',
        )

    def test_notifications_post_fail_no_data(self):
        self._test_post_fail_no_data(
            self.notifications_list,
            self.NOTIFICATIONS_POST_SAMPLE,
            'win',
        )

    def test_customerresponses_post_fail_no_data(self):
        self._test_post_fail_no_data(
            self.customerresponses_list,
            self.CUSTOMER_RESPONSES_POST_SAMPLE,
            'win',
        )

    def test_breakdowns_post_fail_no_data(self):
        self._test_post_fail_no_data(
            self.breakdowns_list,
            self.BREAKDOWNS_POST_SAMPLE,
            'win',
        )

    def test_advisors_post_fail_no_data(self):
        self._test_post_fail_no_data(
            self.advisors_list,
            self.ADVISORS_POST_SAMPLE,
            'team_type',
        )

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def _test_post_fail_bad_data(self, url, data, key, error_msg):
        self._login(signed=True)
        data[key] = 'not valid!'
        response = self.alice_client.post(url, data)
        self.assertEqual(response.status_code, 400)
        content = json.loads(str(response.content, "utf-8"))
        self.assertIn(key, content)
        self.assertEqual(content[key][0], error_msg)

    def test_wins_post_fail_bad_data(self):
        self._test_post_fail_bad_data(
            self.wins_list,
            self.WINS_POST_SAMPLE,
            'customer_email_address',
            'Enter a valid email address.',
        )

    def test_notifications_post_fail_bad_data(self):
        self._test_post_fail_bad_data(
            self.notifications_list,
            self.NOTIFICATIONS_POST_SAMPLE,
            'recipient',
            'Enter a valid email address.',
        )

    def test_customerresponses_post_fail_bad_data(self):
        self._test_post_fail_bad_data(
            self.customerresponses_list,
            self.CUSTOMER_RESPONSES_POST_SAMPLE,
            'win',
            'Incorrect type. Expected pk value, received str.',
        )

    def test_breakdowns_post_fail_bad_data(self):
        self._test_post_fail_bad_data(
            self.breakdowns_list,
            self.BREAKDOWNS_POST_SAMPLE,
            'win',
            'Incorrect type. Expected pk value, received str.',
        )

    def test_advisors_post_fail_bad_data(self):
        self._test_post_fail_bad_data(
            self.advisors_list,
            self.ADVISORS_POST_SAMPLE,
            'team_type',
            '"not valid!" is not a valid choice.',
        )

    def _login(self, signed=False):
        if signed:
            self.alice_client.login(username=self.user.email, password="asdf")
        else:
            self.client.login(username=self.user.email, password="asdf")
