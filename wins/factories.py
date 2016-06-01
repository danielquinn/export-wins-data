import datetime

import factory
import faker

from wins.models import Win
from users.factories import UserFactory


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
