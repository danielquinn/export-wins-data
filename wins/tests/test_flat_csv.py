from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings
import csv
import zipfile
import io
import tempfile

from ..factories import (
    AdvisorFactory,
    BreakdownFactory,
    CustomerResponseFactory,
    NotificationFactory,
    WinFactory,
)
from ..serializers import WinSerializer
from alice.tests.client import AliceClient
from users.factories import UserFactory
from wins.views.flat_csv import CSVView, get_field
from wins.models import Win

class TestFlatCSV(TestCase):

    def setUp(self):
        win = WinFactory()

        BreakdownFactory(win=win)
        AdvisorFactory(win=win)
        CustomerResponseFactory(win=win)
        NotificationFactory(win=win)

        self.url = reverse('csv')
        self.win = win


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
        csv_path = zf.extract('wins.csv', tempfile.mkdtemp())
        with open(csv_path, 'r') as csv_fh:
            win_dict = list(csv.DictReader(csv_fh))[0]
        self._assert_about_win_dict(win_dict)

    def test_direct_call(self):
        win_dict = list(csv.DictReader(CSVView().make_csv().split('\n')))[0]
        self._assert_about_win_dict(win_dict)

    def test_expected_output(self):
        actual_lines = CSVView().make_csv().split('\n')
        expected_lines = '''id,user,Organisation or company name,Company's CDMS Reference,Customer contact name,customer job title,customer email address,Customer or organisation HQ location,What kind of business deal best describes this win?,How was the company supported in achieving this win?,What is the name of their overseas customer?, What are the goods or services that are being exported?,Date business won [MM/YY],country,Type of win,total expected export value,Does the expected export value relate to goods or services?,total expected non export value,sector,Is this win Prosperity Fund related?,"HVO Programme, if applicable",Have HVO Specialists been involved?,Does the win relate to e-exporting?,type of support 1,type of support 2,type of support 3,associated programme 1,associated programme 2,associated programme 3,I confirm that the information above is complete and accurate,My line manager has confirmed the decision to record this win,Lead officer's name,Lead officer's email address,Other officer's email address,Line manager's name,team type,"HQ Team, Region or Post",location,created,advisors,notifications,confirmation,Export breakdown 1,Export breakdown 2,Export breakdown 3,Export breakdown 4,Export breakdown 5,Non-export breakdown 1,Non-export breakdown 2,Non-export breakdown 3,Non-export breakdown 4,Non-export breakdown 5
36a34b29-779a-485d-8f67-b2873aee481d,Edwin Mayo <jlee@gmail.com>,company name,cdms reference,customer name,customer job title,customer@email.address,East Midlands,,description,,,2016-05-25,Canada,Export Win,1,Goods,1,Advanced Engineering,True,AER-01: Global Aerospace,True,True,Market entry advice and support – UKTI/FCO in UK,None,None,None,None,None,True,True,lead officer name,,,line manager name,Trade (TD or ST),TD - Events - Financial & Professional Business Services,location,2016-07-20 13:57:55.979209+00:00,"Name: Billy Bragg, Team DSO - TD - Events - Financial & Professional Business Services, Location: ",True,,2016: 2718281828459.045,,,,,,,,,'''.split('\n')
        
        
        # all headings should match
        self.assertEqual(actual_lines[0].strip('\r'), expected_lines[0])
        
        cols_to_ignore = (0, 1, 38, 53)
        index_colpairs = enumerate(
            zip(actual_lines[1].split(','), expected_lines[1].split(','))
        )
        for index, (actual_col, expected_col) in index_colpairs:
            if index not in cols_to_ignore:
                self.assertEqual(actual_col, expected_col)

    def _assert_about_win_dict(self, win_dict):
        for field_name in WinSerializer().fields:
            try:
                self.assertEquals(
                    win_dict[field_name],
                    str(getattr(self.win, field_name)),
                )
            except:
                try:
                    display_fn = getattr(
                        self.win, "get_{0}_display".format(field_name)
                    )
                except:
                    if field_name == 'date':
                        self.assertEquals(
                            win_dict[get_field(Win, field_name).verbose_name],
                            str(getattr(self.win, field_name))[:10],
                        )
