import csv
import datetime
import io
import tempfile
import zipfile

from django.core.urlresolvers import reverse
from django.test import override_settings, TestCase

from ..serializers import WinSerializer
from ..factories import (
    AdvisorFactory,
    BreakdownFactory,
    CustomerResponseFactory,
    NotificationFactory,
    WIN_TYPES_DICT,
    WinFactory,
)
from alice.tests.client import AliceClient
from users.factories import UserFactory
from wins.views.flat_csv import CSVView


class TestFlatCSV(TestCase):

    def setUp(self):
        user = UserFactory(name='Johnny Fakeman', email="jfakeman@example.com")
        win1 = WinFactory(user=user, id='6e18a056-1a25-46ce-a4bb-0553a912706f')
        BreakdownFactory(
            win=win1,
            year=2016,
            value=10000,
            type=WIN_TYPES_DICT['Export Win'],
        )
        BreakdownFactory(
            win=win1,
            year=2018,
            value=20000,
            type=WIN_TYPES_DICT['Export Win'],
        )
        BreakdownFactory(
            win=win1,
            year=2020,
            value=2000000,
            type=WIN_TYPES_DICT['Export Win'],
        )
        BreakdownFactory(
            win=win1,
            year=2017,
            value=300000,
            type=WIN_TYPES_DICT['Non-Export Win'],
        )
        AdvisorFactory(win=win1)
        AdvisorFactory(
            win=win1,
            name='Bobby Beedle',
            team_type='region',
            hq_team='region:4',
        )
        CustomerResponseFactory(win=win1)
        NotificationFactory(win=win1)
        self.win1 = win1

        # another win with no non-local data
        win2 = WinFactory(user=user, id='6e18a056-1a25-46ce-a4bb-0553a912706d')
        self.win2 = win2

        self.url = reverse('csv')

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_request(self):
        client = AliceClient()
        user = UserFactory.create(is_superuser=True, email='a@b.c')
        user.set_password('asdf')
        user.is_staff = True
        user.save()
        client.login(username=user.email, password='asdf')
        resp = client.get(self.url)
        zf = zipfile.ZipFile(io.BytesIO(resp.content), 'r')
        csv_path = zf.extract('wins_complete.csv', tempfile.mkdtemp())
        with open(csv_path, 'r') as csv_fh:
            win_dict = list(csv.DictReader(csv_fh))[0]
        self._assert_about_win_dict(win_dict)

    def test_direct_call(self):
        win_dict = list(csv.DictReader(CSVView()._make_flat_wins_csv().split('\n')))[0]
        self._assert_about_win_dict(win_dict)

    def test_expected_output(self):
        actual_lines = CSVView()._make_flat_wins_csv().split('\n')
        expected_lines = '''id,user,Organisation or company name,Company's CDMS Reference,Customer contact name,customer job title,customer email address,Customer or organisation HQ location,What kind of business deal best describes this win?,How was the company supported in achieving this win?,What is the name of their overseas customer?, What are the goods or services that are being exported?,Date business won [MM/YY],country,Type of win,total expected export value,total expected non export value,Does the expected export value relate to goods or services?,sector,Is this win Prosperity Fund related?,"HVO Programme, if applicable",Have HVO Specialists been involved?,Does the win relate to e-exporting?,type of support 1,type of support 2,type of support 3,associated programme 1,associated programme 2,associated programme 3,I confirm that the information above is complete and accurate,My line manager has confirmed the decision to record this win,Lead officer's name,Lead officer's email address,Other officer's email address,Line manager's name,team type,"HQ Team, Region or Post",location,created,contributing advisors/team,customer email sent,Export breakdown 1,Export breakdown 2,Export breakdown 3,Export breakdown 4,Export breakdown 5,Non-export breakdown 1,Non-export breakdown 2,Non-export breakdown 3,Non-export breakdown 4,Non-export breakdown 5,customer response recieved,date response received,name,Do you agree with the win details?,comments,How important was our support in securing the win?,Did you gain access to contacts not otherwise accessible?,Did you gain access to information or improved understanding of the country?,Did you improve your profile or credibility in the country?,Did you gain the confidence to explore or expand in the country?,Did you develop and/or nurture critical relationships?,"Did you overcome a problem in the country (eg legal, regulatory, commercial)?","Did the win involve a foreign government or state-owned enterprise (e.g. as a customer, an intermediary or facilitator)?",Was any of the support we provided a prerequisite for the export value to be realised?,Did our support help you achieve this win more quickly than you otherwise would have done?,What proportion of the total expected export value above would you have achieved without our support?,When did your company last export goods and/or services?,"Prior to securing this win, was your company at risk of stopping exporting?","Beyond this win, do you have specific plans to export in the next 12 months?",Has this win enabled you to expand into a new market?,Has this win enabled you to increase exports as a % of your turnover?,Has this win enabled you to maintain or expand in an existing market?,Would be willing to have your success featured as a UKTI / Exporting is GREAT case study?\r
6e18a056-1a25-46ce-a4bb-0553a912706f,Johnny Fakeman <jfakeman@example.com>,company name,cdms reference,customer name,customer job title,customer@email.address,East Midlands,,description,,,2016-05-25,Canada,Export Win,"100,000","2,300",Goods,Advanced Engineering,Yes,AER-01: Global Aerospace,Yes,Yes,Market entry advice and support – UKTI/FCO in UK,,,,,,Yes,Yes,lead officer name,,,line manager name,Trade (TD or ST),TD - Events - Financial & Professional Business Services,location,{created1},"Name: Billy Bragg, Team DSO - TD - Events - Financial & Professional Business Services, Location: N/A, Name: Bobby Beedle, Team UK Region - North East, Location: N/A",Yes,"2016: 10,000","2018: 20,000","2020: 2,000,000",,,"2017: 300,000",,,,,Yes,{response_date},Cakes,Yes,Good work,1,2,3,4,5,1,2,Yes,No,Yes,Would have achieved 80% of the export value without your support,Last 12 months,No,Yes,No,Yes,No,No\r
6e18a056-1a25-46ce-a4bb-0553a912706d,Johnny Fakeman <jfakeman@example.com>,company name,cdms reference,customer name,customer job title,customer@email.address,East Midlands,,description,,,2016-05-25,Canada,Export Win,"100,000","2,300",Goods,Advanced Engineering,Yes,AER-01: Global Aerospace,Yes,Yes,Market entry advice and support – UKTI/FCO in UK,,,,,,Yes,Yes,lead officer name,,,line manager name,Trade (TD or ST),TD - Events - Financial & Professional Business Services,location,{created2},,No,,,,,,,,,,,No,,,,,,,,,,,,,,,,,,,,,,\r'''\
            .format(
                created1=self.win1.created,
                created2=self.win2.created,
                response_date=self.win1.confirmation.created,
            ).split('\n')

        for actual_line, expected_line in zip(actual_lines, expected_lines):
            zipped_cols = zip(actual_line.split(','), expected_line.split(','))
            for actual_col, expected_col in zipped_cols:
                self.assertEqual(actual_col, expected_col)

    def _val_to_str(self, val):
        return CSVView()._val_to_str(val)

    def _assert_about_win_dict(self, win_dict):
        for field_name in WinSerializer().fields:
            field = CSVView()._get_win_field(field_name)
            csv_name = field.verbose_name or field.name
            try:
                comma_fields = [
                    'total_expected_export_value',
                    'total_expected_non_export_value',
                ]
                value = getattr(self.win1, field_name)
                if field_name in comma_fields:
                    value = "{:,}".format(value)
                self.assertEquals(
                    win_dict[csv_name],
                    self._val_to_str(value),
                )
            except AssertionError:
                try:
                    display_fn = getattr(
                        self.win1, "get_{0}_display".format(field_name)
                    )
                    self.assertEquals(
                        win_dict[csv_name],
                        self._val_to_str(display_fn()),
                    )
                except (AttributeError, AssertionError):
                    if field_name == 'date':
                        self.assertEquals(
                            win_dict[csv_name],
                            str(getattr(self.win1, field_name))[:10],
                        )
                    elif field_name == 'created':
                        self.assertEquals(
                            win_dict[csv_name],
                            str(getattr(self.win1, field_name)),
                        )
                    else:
                        raise Exception
