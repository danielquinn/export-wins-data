from datetime import date
import factory
import json

from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from rest_framework.authtoken.models import Token

from users.models import User
from wins.models import Win


class UserFactory(factory.Factory):
    class Meta(object):
        model = User


class WinFactory(factory.Factory):

    class Meta(object):
        model = Win

    customer_location = 1
    type = 1
    date = date(2016, 5, 17)
    total_expected_export_value = 1
    goods_vs_services = 1
    total_expected_non_export_value = 1
    sector = 1
    is_prosperity_fund_related = True
    hvo_programme = 1
    has_hvo_specialist_involvement = True
    is_e_exported = True
    type_of_support_1 = 1
    is_personally_confirmed = True
    is_line_manager_confirmed = True
    team_type = 1
    country = "CA"


class AlicePermissionTestCase(TestCase):

    WINS_SCHEMA = "{}schema/".format(reverse("drf:win-list"))
    WINS_LIST = reverse("drf:win-list")
    WINS_DETAIL = reverse("drf:win-detail", kwargs={"pk": 1})

    POST_SAMPLE = {
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
      "hq_team": "hq team, region, or post",
      "hvo_programme": 1,
      "is_e_exported": True,
      "is_line_manager_confirmed": True,
      "is_personally_confirmed": True,
      "is_prosperity_fund_related": True,
      "lead_officer_name": "lead officer name",
      "line_manager_name": "line manager name",
      "location": "Edinburgh, UK",
      "sector": 1,
      "team_type": 1,
      "total_expected_export_value": 5,
      "total_expected_non_export_value": 5,
      "type": 1,
      "type_of_support_1": 1,
    }

    def setUp(self):

        self.client = Client()

        self.user = UserFactory.create()
        self.superuser = UserFactory.create(is_superuser=True, email="a@b.c")

        # I can't for the life of me determine why this is necessary
        self.user.save()
        self.superuser.save()

        self.user_token = Token.objects.create(user=self.user)
        self.superuser_token = Token.objects.create(user=self.superuser)

        WinFactory.create().save()

    # GET Schema --------------------------------------------------------------

    def test_get_schema_pass(self):

        with self.settings(UI_SECRET="secret"):
            response = self.client.get(
                self.WINS_SCHEMA,
                HTTP_X_SIGNATURE="f340fc87b8a521e6bd7ba1186af54871eab1e45e35b9"
                                 "f96720c2b9911b231803"
            )

        content = json.loads(str(response.content, "utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["id"]["label"], "ID")

    def test_get_schema_fail(self):
        with self.settings(UI_SECRET="secret"):
            response = self.client.get(self.WINS_SCHEMA)
        self.assertEqual(response.status_code, 401)

    # GET List ----------------------------------------------------------------

    def test_get_list_pass(self):
        auth = {
            "HTTP_AUTHORIZATION": "Token {}".format(self.user_token),
            "HTTP_X_SIGNATURE": "1e76bd6dc832dde1bf824726f00d5261c685b644adddb"
                                "3c2738a535a088ac77a",
        }
        with self.settings(UI_SECRET="secret"):
            response = self.client.get(self.WINS_LIST, **auth)
        self.assertEqual(response.status_code, 200)

    def test_get_list_fail(self):
        auth = {
        }
        with self.settings(UI_SECRET="secret"):
            response = self.client.get(reverse("drf:win-list"), **auth)
        self.assertEqual(response.status_code, 401)

    def test_get_list_fail_no_signature(self):
        auth = {"HTTP_AUTHORIZATION": "Token {}".format(self.user_token)}
        with self.settings(UI_SECRET="secret"):
            response = self.client.get(self.WINS_LIST, **auth)
        self.assertEqual(response.status_code, 403)

    def test_get_list_fail_bad_signature(self):
        auth = {
            "HTTP_AUTHORIZATION": "Token {}".format(self.user_token),
            "HTTP_X_SIGNATURE": "bad-signature",
        }
        with self.settings(UI_SECRET="secret"):
            response = self.client.get(self.WINS_LIST, **auth)
        self.assertEqual(response.status_code, 403)

    def test_get_list_fail_no_auth(self):
        auth = {
            "HTTP_X_SIGNATURE": "1e76bd6dc832dde1bf824726f00d5261c685b644adddb"
                                "3c2738a535a088ac77a",
        }
        with self.settings(UI_SECRET="secret"):
            response = self.client.get(self.WINS_LIST, **auth)
        self.assertEqual(response.status_code, 401)

    # GET Detail --------------------------------------------------------------

    def test_get_detail_pass(self):
        auth = {
            "HTTP_AUTHORIZATION": "Token {}".format(self.user_token),
            "HTTP_X_SIGNATURE": "3890a6c0dfaaf2afa5e8bf284f4398f833009d9014edf"
                                "986b856c89c979d0cbe",
        }
        with self.settings(UI_SECRET="secret"):
            response = self.client.get(self.WINS_DETAIL, **auth)
        self.assertEqual(response.status_code, 200)

    def test_get_detail_fail(self):
        auth = {
        }
        with self.settings(UI_SECRET="secret"):
            response = self.client.get(self.WINS_DETAIL, **auth)
        self.assertEqual(response.status_code, 401)

    def test_get_detail_fail_no_signature(self):
        auth = {"HTTP_AUTHORIZATION": "Token {}".format(self.user_token)}
        with self.settings(UI_SECRET="secret"):
            response = self.client.get(self.WINS_DETAIL, **auth)
        self.assertEqual(response.status_code, 403)

    def test_get_detail_fail_bad_signature(self):
        auth = {
            "HTTP_AUTHORIZATION": "Token {}".format(self.user_token),
            "HTTP_X_SIGNATURE": "bad-signature",
        }
        with self.settings(UI_SECRET="secret"):
            response = self.client.get(self.WINS_DETAIL, **auth)
        self.assertEqual(response.status_code, 403)

    def test_get_detail_fail_no_auth(self):
        auth = {
            "HTTP_X_SIGNATURE": "1e76bd6dc832dde1bf824726f00d5261c685b644adddb"
                                "3c2738a535a088ac77a",
        }
        with self.settings(UI_SECRET="secret"):
            response = self.client.get(self.WINS_DETAIL, **auth)
        self.assertEqual(response.status_code, 401)

    # POST --------------------------------------------------------------------

    def test_post_pass(self):
        auth = {
            "HTTP_AUTHORIZATION": "Token {}".format(self.user_token),
            "HTTP_X_SIGNATURE": "how-do-i-get-this-signature?",
        }
        data = self.POST_SAMPLE
        with self.settings(UI_SECRET="secret"):
            response = self.client.post(self.WINS_LIST, data, **auth)
        self.assertEqual(response.status_code, 201)

    def test_post_fail_no_auth(self):
        pass

    def test_post_fail_bad_auth(self):
        pass

    def test_post_fail_no_signature(self):
        pass

    def test_post_fail_bad_signature(self):
        pass

    def test_post_fail_no_data(self):
        pass

    def test_post_fail_bad_data(self):
        pass
