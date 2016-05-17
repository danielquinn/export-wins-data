from django.db import models
from django_countries.fields import CountryField

from .constants import (
    TYPES, UK_REGIONS, GOODS_VS_SERVICES, SECTORS, HVO_PROGRAMMES,
    TYPES_OF_SUPPORT, TEAMS, PROGRAMMES, RATINGS, WITHOUT_OUR_SUPPORT,
    EXPERIENCE
)


class Win(models.Model):

    class Meta(object):
        verbose_name = "Export Win"
        verbose_name_plural = "Export Wins"

    company_name = models.CharField(max_length=128)
    cdms_reference = models.CharField(
        max_length=128, verbose_name="Company's CDMS Reference")

    customer_name = models.CharField(max_length=128)
    customer_job_title = models.CharField(max_length=128)
    customer_email_address = models.EmailField()
    customer_location = models.PositiveIntegerField(choices=UK_REGIONS)

    description = models.TextField(
        verbose_name="Brief description of win",
        help_text="Describe the Win. What sort of business deal best "
                  "describes this Win? Include details of the contract or "
                  "order, what goods/services are included, the name of the "
                  "overseas customer and the support provided by UKTI/FCO."
    )

    type = models.PositiveIntegerField(
        choices=TYPES, verbose_name="Type of win")
    date = models.DateField(verbose_name="Date business won [MM/YY]")
    country = CountryField()

    total_expected_export_value = models.IntegerField()
    goods_vs_services = models.PositiveIntegerField(
        choices=GOODS_VS_SERVICES,
        verbose_name="Does the Export value relate to goods or services?"
    )
    total_expected_non_export_value = models.IntegerField()

    sector = models.PositiveIntegerField(choices=SECTORS)
    is_prosperity_fund_related = models.BooleanField()
    hvo_programme = models.PositiveIntegerField(
        choices=HVO_PROGRAMMES, verbose_name="HVO Programme")
    has_hvo_specialist_involvement = models.BooleanField()
    is_e_exported = models.BooleanField()

    type_of_support_1 = models.PositiveIntegerField(choices=TYPES_OF_SUPPORT)
    type_of_support_2 = models.PositiveIntegerField(choices=TYPES_OF_SUPPORT,
                                                    blank=True, null=True)
    type_of_support_3 = models.PositiveIntegerField(choices=TYPES_OF_SUPPORT,
                                                    blank=True, null=True)

    associated_programme_1 = models.PositiveIntegerField(choices=PROGRAMMES,
                                                         blank=True, null=True)
    associated_programme_2 = models.PositiveIntegerField(choices=PROGRAMMES,
                                                         blank=True, null=True)
    associated_programme_3 = models.PositiveIntegerField(choices=PROGRAMMES,
                                                         blank=True, null=True)

    is_personally_confirmed = models.BooleanField(
        verbose_name="I confirm that the information above is complete and "
                     "accurate"
    )
    is_line_manager_confirmed = models.BooleanField(
        verbose_name="My line manager has seen and confirmed this information")

    lead_officer_name = models.CharField(max_length=128)
    line_manager_name = models.CharField(max_length=128)
    team_type = models.PositiveIntegerField(choices=TEAMS)
    hq_team = models.CharField(
        max_length=128,
        verbose_name="HQ Team, Region or Post"
    )
    location = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)


class Breakdown(models.Model):

    TYPE_EXPORT = 1
    TYPE_NON_EXPORT = 2
    TYPES = (
        (TYPE_EXPORT, "Export"),
        (TYPE_NON_EXPORT, "Non-export"),
    )

    win = models.ForeignKey(Win, related_name="breakdowns")
    type = models.PositiveIntegerField(choices=TYPES)
    year = models.PositiveIntegerField()
    value = models.PositiveIntegerField()

    def __str__(self):
        return "{}/{}: {}".format(
            self.year, str(self.year + 1)[:-2], self.value / 100)


class Advisor(models.Model):
    """
    At least one!
    Should this be n:1 or 1:1? The latter is easier, but there's no sense in
    doing that if we'll just have to change it soon.
    """

    name = models.CharField(max_length=128)
    team_type = models.PositiveIntegerField(choices=TEAMS)
    hq_team = models.CharField(max_length=128)
    location = models.CharField(
        max_length=128, verbose_name="Location (if applicable)")


class CustomerResponse(models.Model):

    win = models.OneToOneField(Win)

    access_to_contacts = models.PositiveIntegerField(
        choices=RATINGS,
        verbose_name="Gained access to contacts not otherwise accessible"
    )
    access_to_information = models.PositiveIntegerField(
        choices=RATINGS,
        verbose_name="Gained access to information or improved understanding "
                     "of the country"
    )
    improved_profile = models.PositiveIntegerField(
        choices=RATINGS,
        verbose_name="Improved your profile or credibility in the country"
    )
    gained_confidence = models.PositiveIntegerField(
        choices=RATINGS,
        verbose_name="Gained the confidence to explore or expand in the "
                     "country"
    )
    developed_relationships = models.PositiveIntegerField(
        choices=RATINGS,
        verbose_name="Developed and/or nurtured critical relationships"
    )
    overcame_problem = models.PositiveIntegerField(
        choices=RATINGS,
        verbose_name="Overcame a problem in the country (eg legal, "
                     "regulatory, commercial)"
    )

    involved_state_enterprise = models.BooleanField(
        verbose_name="Did the Win involve a foreign government or state-owned "
                     "enterprise? (e.g. as a customer, an intermediary or "
                     "facilitator)"
    )
    interventions_were_prerequisite = models.BooleanField(
        verbose_name="Were any of the interventions needed for this Win a "
                     "pre-requisite for the export value to be realised?"
    )
    support_improved_speed = models.BooleanField(
        verbose_name="Did our support or intervention(s) help you achieve "
                     "this Win more quickly than you otherwise would have "
                     "done?"
    )
    expected_portion_without_help = models.PositiveIntegerField(
        choices=WITHOUT_OUR_SUPPORT,
        verbose_name="What proportion of the total expected export value of "
                     "this Win would you have achieved without our support?"
    )
    last_export = models.PositiveIntegerField(
        choices=EXPERIENCE,
        verbose_name="When did your company last export goods and/or services?"
    )
    company_was_at_risk_of_not_exporting = models.BooleanField(
        verbose_name="Prior to securing this Win, was your company at risk of"
                     "not exporting?"
    )
    has_explicit_export_plans = models.BooleanField(
        verbose_name="Do you have specific plans to export in the next 12"
                     "months?"
    )
    has_enabled_expansion_into_new_market = models.BooleanField(
        verbose_name="Has this Win enabled you to expand into a new market?"
    )
    has_increased_exports_as_percent_of_turnover = models.BooleanField(
        verbose_name="Has this Win enabled you to increase exports as a % of"
                     "your turnover?"
    )
    has_enabled_expansion_into_existing_market = models.BooleanField(
        verbose_name="Has this Win enabled you to expand into an existing"
                     "market?"
    )
    comments = models.TextField(blank=True)
    name = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
