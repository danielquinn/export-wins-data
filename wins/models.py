import uuid

from django.db import models
from django_countries.fields import CountryField

from users.models import User
from . import constants


class Win(models.Model):
    """ Information about a given "export win", submitted by an officer """

    class Meta(object):
        verbose_name = "Export Win"
        verbose_name_plural = "Export Wins"

    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey(User, related_name="wins")
    company_name = models.CharField(
        max_length=128, verbose_name="Organisation or company name")
    cdms_reference = models.CharField(
        max_length=128, verbose_name="Company's CDMS Reference")

    customer_name = models.CharField(
        max_length=128, verbose_name="Customer contact name")
    customer_job_title = models.CharField(max_length=128)
    customer_email_address = models.EmailField()
    customer_location = models.PositiveIntegerField(
        choices=constants.UK_REGIONS,
        verbose_name="Customer or organisation HQ location"
    )

    business_type = models.CharField(
        max_length=128,
        verbose_name="What kind of business deal best describes this win?",
    )
    # Formerly a catch-all, since broken out into business_type,
    # name_of_customer, name_of_export and description.
    description = models.TextField(
        verbose_name="How was the company supported in achieving this win?",
    )
    name_of_customer = models.CharField(
        max_length=128,
        verbose_name="What is the name of their overseas customer?",
    )
    name_of_export = models.CharField(
        max_length=128,
        verbose_name=" What are the goods or services that are being exported?",
    )

    type = models.PositiveIntegerField(
        choices=constants.WIN_TYPES, verbose_name="Type of win")
    date = models.DateField(verbose_name="Date business won [MM/YY]")
    country = CountryField()

    total_expected_export_value = models.IntegerField()
    goods_vs_services = models.PositiveIntegerField(
        choices=constants.GOODS_VS_SERVICES,
        verbose_name="Does the expected export value relate to goods or "
                     "services?"
    )
    total_expected_non_export_value = models.IntegerField()

    sector = models.PositiveIntegerField(choices=constants.SECTORS)
    is_prosperity_fund_related = models.BooleanField(
        verbose_name="Is this win Prosperity Fund related?")
    hvo_programme = models.CharField(
        max_length=6,
        choices=constants.HVO_PROGRAMMES,
        verbose_name="HVO Programme, if applicable",
        blank=True,
        null=True
    )
    has_hvo_specialist_involvement = models.BooleanField(
        verbose_name="Have HVO Specialists been involved?")
    is_e_exported = models.BooleanField("Does the win relate to e-exporting?")

    type_of_support_1 = models.PositiveIntegerField(choices=constants.TYPES_OF_SUPPORT)
    type_of_support_2 = models.PositiveIntegerField(
        choices=constants.TYPES_OF_SUPPORT, blank=True, null=True)
    type_of_support_3 = models.PositiveIntegerField(
        choices=constants.TYPES_OF_SUPPORT, blank=True, null=True)

    associated_programme_1 = models.PositiveIntegerField(
        choices=constants.PROGRAMMES, blank=True, null=True)
    associated_programme_2 = models.PositiveIntegerField(
        choices=constants.PROGRAMMES, blank=True, null=True)
    associated_programme_3 = models.PositiveIntegerField(
        choices=constants.PROGRAMMES, blank=True, null=True)

    is_personally_confirmed = models.BooleanField(
        verbose_name="I confirm that the information above is complete and "
                     "accurate"
    )
    is_line_manager_confirmed = models.BooleanField(
        verbose_name="My line manager has confirmed the decision to record "
                     "this win"
    )

    lead_officer_name = models.CharField(
        max_length=128,
        verbose_name="Lead officer's name",
        help_text="This is the name that will be included in the email to the "
                  "customer"
    )

    lead_officer_email_address = models.EmailField(
        verbose_name="Lead officer's email address",
        blank=True
    )
    other_official_email_address = models.EmailField(
        verbose_name="Other officer's email address",
        blank=True
    )
    line_manager_name = models.CharField(
        max_length=128, verbose_name="Line manager's name")
    team_type = models.CharField(max_length=128, choices=constants.TEAMS)
    hq_team = models.CharField(
        max_length=128,
        verbose_name="HQ Team, Region or Post",
        choices=constants.HQ_TEAM_REGION_OR_POST
    )
    location = models.CharField(max_length=128, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    complete = models.BooleanField()

    def __str__(self):
        return "Export win {}: {} - {}".format(
            self.pk,
            self.user,
            self.created.strftime("%Y-%m-%d %H:%M:%S"),
        )

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4())
        models.Model.save(self, *args, **kwargs)

    @property
    def target_addresses(self):
        addresses = [self.user.email]
        if self.lead_officer_email_address:
            addresses.append(self.lead_officer_email_address)
        if self.other_official_email_address:
            addresses.append(self.other_official_email_address)
        return tuple(set(addresses))


class Breakdown(models.Model):
    """ Export/non-export value broken down by given year

    Totals found in win model as `total_expected_export_value` and
    `total_expected_non_export_value`.
    """

    TYPE_EXPORT = {y: x for x, y in constants.BREAKDOWN_TYPES}['Export']

    class Meta:
        ordering = ["year"]

    win = models.ForeignKey(Win, related_name="breakdowns")
    type = models.PositiveIntegerField(choices=constants.BREAKDOWN_TYPES)
    year = models.PositiveIntegerField()
    value = models.PositiveIntegerField()

    def __str__(self):
        return "{}/{} {}: {}K".format(
            self.year,
            str(self.year + 1)[-2:],
            dict(constants.BREAKDOWN_TYPES)[self.type],
            self.value / 1000,
        )


class Advisor(models.Model):

    win = models.ForeignKey(Win, related_name="advisors")
    name = models.CharField(max_length=128)
    team_type = models.CharField(max_length=128, choices=constants.TEAMS)
    hq_team = models.CharField(
        max_length=128,
        verbose_name="HQ Team, Region or Post",
        choices=constants.HQ_TEAM_REGION_OR_POST
    )
    location = models.CharField(
        max_length=128,
        verbose_name="Location (if applicable)",
        blank=True,
    )

    def __str__(self):
        return "Name: {0}, Team {1} - {2}, Location: {3}".format(
            self.name,
            dict(constants.TEAMS)[self.team_type],
            dict(constants.HQ_TEAM_REGION_OR_POST)[self.hq_team],
            self.location or 'N/A',
        )


class CustomerResponse(models.Model):
    """ Customer's response to being asked about a Win (aka Confirmation) """

    win = models.OneToOneField(Win, related_name="confirmation")

    our_support = models.PositiveIntegerField(
        choices=constants.RATINGS,
        verbose_name="How important was our support in securing the win?"
    )
    access_to_contacts = models.PositiveIntegerField(
        choices=constants.RATINGS,
        verbose_name="Did you gain access to contacts not otherwise accessible?"
    )
    access_to_information = models.PositiveIntegerField(
        choices=constants.RATINGS,
        verbose_name="Did you gain access to information or improved "
                     "understanding of the country?"
    )
    improved_profile = models.PositiveIntegerField(
        choices=constants.RATINGS,
        verbose_name="Did you improve your profile or credibility in the "
                     "country?"
    )
    gained_confidence = models.PositiveIntegerField(
        choices=constants.RATINGS,
        verbose_name="Did you gain the confidence to explore or expand in the "
                     "country?"
    )
    developed_relationships = models.PositiveIntegerField(
        choices=constants.RATINGS,
        verbose_name="Did you develop and/or nurture critical relationships?"
    )
    overcame_problem = models.PositiveIntegerField(
        choices=constants.RATINGS,
        verbose_name="Did you overcome a problem in the country (eg legal, "
                     "regulatory, commercial)?"
    )

    involved_state_enterprise = models.BooleanField(
        verbose_name="Did the win involve a foreign government or state-owned "
                     "enterprise (e.g. as a customer, an intermediary or "
                     "facilitator)?",
        default=False
    )
    interventions_were_prerequisite = models.BooleanField(
        verbose_name="Was any of the support we provided a prerequisite for "
                     "the export value to be realised?",
        default=False
    )
    support_improved_speed = models.BooleanField(
        verbose_name="Did our support help you achieve "
                     "this win more quickly than you otherwise would have "
                     "done?",
        default=False
    )
    expected_portion_without_help = models.PositiveIntegerField(
        choices=constants.WITHOUT_OUR_SUPPORT,
        verbose_name="What proportion of the total expected export value "
                     "above would you have achieved without our support?"
    )
    last_export = models.PositiveIntegerField(
        choices=constants.EXPERIENCE,
        verbose_name="When did your company last export goods and/or services?"
    )
    company_was_at_risk_of_not_exporting = models.BooleanField(
        verbose_name="Prior to securing this win, was your company at risk of "
                     "stopping exporting?",
        default=False
    )
    has_explicit_export_plans = models.BooleanField(
        verbose_name="Beyond this win, do you have specific plans to export "
                     "in the next 12 months?",
        default=False
    )
    has_enabled_expansion_into_new_market = models.BooleanField(
        verbose_name="Has this win enabled you to expand into a new market?",
        default=False
    )
    has_increased_exports_as_percent_of_turnover = models.BooleanField(
        verbose_name="Has this win enabled you to increase exports as a % of "
                     "your turnover?",
        default=False
    )
    has_enabled_expansion_into_existing_market = models.BooleanField(
        verbose_name="Has this win enabled you to maintain or expand in an "
                     "existing market?",
        default=False
    )
    # temporarily nullable for migration - should ultimately be filled in and
    # turned into a BooleanField
    agree_with_win = models.NullBooleanField(
        verbose_name="Do you agree with the win details?",
    )
    case_study_willing = models.BooleanField(
        verbose_name="Would be willing to have your success featured as a UKTI "
                     "/ Exporting is GREAT case study?"
    )

    comments = models.TextField(blank=True)
    name = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Customer response to {}".format(self.win)


class Notification(models.Model):
    """ Record when notifications sent (for analysis and sending followups) """

    TYPE_OFFICER = {y: x for x, y in constants.NOTIFICATION_TYPES}['Officer']
    TYPE_CUSTOMER = {y: x for x, y in constants.NOTIFICATION_TYPES}['Customer']

    win = models.ForeignKey(Win, related_name="notifications")
    user = models.ForeignKey(
        User, blank=True, null=True, related_name="notifications")
    recipient = models.EmailField()
    type = models.CharField(max_length=1, choices=constants.NOTIFICATION_TYPES)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0} notification to {1} regarding Win {2} sent {3}".format(
            dict(constants.NOTIFICATION_TYPES)[self.type],
            self.recipient,
            self.win.id,
            self.created
        )
