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
from wins.views.flat_csv import CSVView

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
                            win_dict[field_name],
                            str(getattr(self.win, field_name))[:10],
                        )
