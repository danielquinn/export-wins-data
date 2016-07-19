import datetime

import factory
import faker

from wins.models import Win, Breakdown, Advisor, CustomerResponse, Notification
from wins.constants import WIN_TYPES
from users.factories import UserFactory

TYPES_DICT = {y: x for x, y in WIN_TYPES}

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


class BreakdownFactory(factory.DjangoModelFactory):

    class Meta:
        model = Breakdown

    type = TYPES_DICT['Export Win']
    year = 2016
    value = 2718281828459045


class AdvisorFactory(factory.DjangoModelFactory):

    class Meta:
        model = Advisor

    name = 'Billy Bragg'
    team_type = 'dso'
    hq_team = 'team:1'


class CustomerResponseFactory(factory.DjangoModelFactory):

    class Meta:
        model = CustomerResponse

    our_support = 1
    access_to_contacts = 1
    access_to_information = 1
    improved_profile = 1
    gained_confidence = 1
    developed_relationships = 1
    overcame_problem = 1

    involved_state_enterprise = True
    interventions_were_prerequisite = True
    support_improved_speed = True
    expected_portion_without_help = 1
    last_export = 1
    company_was_at_risk_of_not_exporting = True
    has_explicit_export_plans = True
    has_enabled_expansion_into_new_market = True
    has_increased_exports_as_percent_of_turnover = True
    has_enabled_expansion_into_existing_market = True
    case_study_willing = True

    name = 'Cakes'


class NotificationFactory(factory.DjangoModelFactory):

    class Meta:
        model = Notification

    recipient = 'a@b.com'
    type = 'c'
