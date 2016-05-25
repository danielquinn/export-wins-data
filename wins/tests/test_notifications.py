import datetime
import factory
import faker

from django.test import TestCase, Client, override_settings

from alice.tests.client import AliceClient
from users.models import User

from ..models import Win, Notification


fake = faker.Factory.create()


class UserFactory(factory.DjangoModelFactory):
    class Meta(object):
        model = User

    email = factory.lazy_attribute(lambda o: fake.email())


class WinFactory(factory.DjangoModelFactory):
    class Meta(object):
        model = Win

    user = factory.SubFactory(UserFactory)
    company_name = "company name"
    cdms_reference = "cdms reference"

    customer_name = "customer name"
    customer_job_title = "customer job title"
    customer_email_address = "customer@email.address"
    customer_location = 1

    description = "description"

    type = 1
    date = datetime.datetime(2016, 5, 25)
    country = "CA"

    total_expected_export_value = 1
    goods_vs_services = 1
    total_expected_non_export_value = 1

    sector = 1
    is_prosperity_fund_related = True
    hvo_programme = "AER-01"
    has_hvo_specialist_involvement = True
    is_e_exported = True

    type_of_support_1 = 1

    is_personally_confirmed = True
    is_line_manager_confirmed = True

    lead_officer_name = "lead officer name"
    line_manager_name = "line manager name"
    team_type = "team"
    hq_team = "team:1"
    location = "location"


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
