from hashlib import sha256

import factory
import json

from django.test import TestCase, Client, override_settings
from django.core.urlresolvers import reverse

from rest_framework.authtoken.models import Token

from users.models import User

from .client import AliceClient


class UserFactory(factory.Factory):
    class Meta(object):
        model = User


class AlicePermissionTestCase(TestCase):

    POST_SAMPLE = {
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

    def setUp(self):

        self.client = Client()
        self.alice_client = AliceClient()

        self.user = UserFactory.create()
        self.superuser = UserFactory.create(is_superuser=True, email="a@b.c")

        # I can't for the life of me determine why this is necessary
        self.user.save()
        self.superuser.save()

        self.user_token = Token.objects.create(user=self.user)
        self.superuser_token = Token.objects.create(user=self.superuser)

        self.wins_schema = reverse("drf:win-schema")
        self.wins_list = reverse("drf:win-list")
        self.wins_detail = reverse("drf:win-detail", kwargs={
            "pk": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        })

    # GET Schema --------------------------------------------------------------

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_get_schema_pass(self):
        response = self.alice_client.get(self.wins_schema)
        content = json.loads(str(response.content, "utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["id"]["label"], "Id")

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_get_schema_fail(self):
        response = self.client.get(self.wins_schema)
        self.assertEqual(response.status_code, 401)

    # GET List ----------------------------------------------------------------

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_get_list_pass(self):
        auth = {"HTTP_AUTHORIZATION": "Token {}".format(self.user_token)}
        response = self.alice_client.get(self.wins_list, **auth)
        self.assertEqual(response.status_code, 200)

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_get_list_fail(self):
        response = self.alice_client.get(reverse("drf:win-list"))
        self.assertEqual(response.status_code, 401)

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_get_list_fail_no_signature(self):
        auth = {"HTTP_AUTHORIZATION": "Token {}".format(self.user_token)}
        response = self.client.get(self.wins_list, **auth)
        self.assertEqual(response.status_code, 403)

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_get_list_fail_bad_signature(self):
        auth = {
            "HTTP_AUTHORIZATION": "Token {}".format(self.user_token),
            "HTTP_X_SIGNATURE": "bad-signature",
        }
        response = self.alice_client.get(self.wins_list, **auth)
        self.assertEqual(response.status_code, 403)

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_get_list_fail_no_auth(self):
        response = self.alice_client.get(self.wins_list)
        self.assertEqual(response.status_code, 401)

    # GET Detail --------------------------------------------------------------

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_get_detail_pass(self):
        auth = {"HTTP_AUTHORIZATION": "Token {}".format(self.user_token)}
        response = self.alice_client.get(self.wins_detail, **auth)
        self.assertEqual(response.status_code, 404)

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_get_detail_fail(self):
        response = self.alice_client.get(self.wins_detail)
        self.assertEqual(response.status_code, 401)

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_get_detail_fail_no_signature(self):
        auth = {"HTTP_AUTHORIZATION": "Token {}".format(self.user_token)}
        response = self.client.get(self.wins_detail, **auth)
        self.assertEqual(response.status_code, 403)

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_get_detail_fail_bad_signature(self):
        auth = {
            "HTTP_AUTHORIZATION": "Token {}".format(self.user_token),
            "HTTP_X_SIGNATURE": "bad-signature",
        }
        response = self.alice_client.get(self.wins_detail, **auth)
        self.assertEqual(response.status_code, 403)

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_get_detail_fail_no_auth(self):
        response = self.alice_client.get(self.wins_detail)
        self.assertEqual(response.status_code, 401)

    # POST --------------------------------------------------------------------

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_post_pass(self):
        auth = {"HTTP_AUTHORIZATION": "Token {}".format(self.user_token)}
        data = self.POST_SAMPLE
        response = self.alice_client.post(self.wins_list, data, **auth)
        self.assertEqual(response.status_code, 201, response.content)

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_post_fail_no_auth(self):
        data = self.POST_SAMPLE
        response = self.alice_client.post(self.wins_list, data)
        self.assertEqual(response.status_code, 401)

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_post_fail_bad_auth(self):
        auth = {"HTTP_AUTHORIZATION": "Token bad-auth"}
        data = self.POST_SAMPLE
        response = self.alice_client.post(self.wins_list, data, **auth)
        self.assertEqual(response.status_code, 401)

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_post_fail_no_signature(self):
        auth = {"HTTP_AUTHORIZATION": "Token {}".format(self.user_token)}
        data = self.POST_SAMPLE
        response = self.client.post(self.wins_list, data, **auth)
        self.assertEqual(response.status_code, 403)

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_post_fail_bad_signature(self):
        auth = {
            "HTTP_AUTHORIZATION": "Token {}".format(self.user_token),
            "HTTP_X_SIGNATURE": "bad-signature"
        }
        data = self.POST_SAMPLE
        response = self.alice_client.post(self.wins_list, data, **auth)
        self.assertEqual(response.status_code, 403)

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_post_fail_no_data(self):
        auth = {"HTTP_AUTHORIZATION": "Token {}".format(self.user_token)}
        response = self.alice_client.post(self.wins_list, {}, **auth)
        self.assertEqual(response.status_code, 400)

        content = json.loads(str(response.content, "utf-8"))
        self.assertTrue("customer_email_address" in content)
        self.assertEqual(
            content["customer_email_address"],
            ["This field is required."]
        )

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_post_fail_bad_data(self):

        auth = {"HTTP_AUTHORIZATION": "Token {}".format(self.user_token)}

        data = self.POST_SAMPLE.copy()
        data["customer_email_address"] = "not an email address"
        response = self.alice_client.post(self.wins_list, data, **auth)
        self.assertEqual(response.status_code, 400)

        content = json.loads(str(response.content, "utf-8"))
        self.assertTrue("customer_email_address" in content)
        self.assertEqual(
            content["customer_email_address"],
            ["Enter a valid email address."]
        )
