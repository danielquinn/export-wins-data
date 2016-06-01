from unittest import mock

from django.test import TestCase, Client, override_settings, RequestFactory
from django.core.urlresolvers import reverse

from ..authenticators import (
    SignatureMixin, AlicePermission, SignatureOnlyAlicePermission
    )
from .client import AliceClient


class BaseSignatureTestCase(TestCase):
    """
    Base TestCase providing a mock request and appropriate signature
    """

    def setUp(self):
        self.request = RequestFactory().get('/path')
        self.request._body = b'lol'
        # signature generated from the key in settings, and above path & body
        self.sig = (
            '25dc2f24f29c589a88baa22fa9aebbd58c5acb338f15ff920a752a9e414ba47e'
        )


class SignatureMixinTestCase(BaseSignatureTestCase):

    def setUp(self):
        super().setUp()
        self.sig_mixin = SignatureMixin()

    def test_generate_signature(self):
        signature = self.sig_mixin._generate_signature(
            'secret',
            'path',
            b'body',
        )
        self.assertEqual(
            signature,
            'c6be1984f8b516e94d7257031cc47ed9863a433e461ac0117214b1b6a7801991',
        )

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_test_signature_missing(self):
        self.assertFalse(self.sig_mixin._test_signature(self.request))

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_test_signature_incorrect(self):
        self.request.META['HTTP_X_SIGNATURE'] = 'bad-signature'
        self.assertFalse(self.sig_mixin._test_signature(self.request))

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_test_signature_correct(self):
        self.request.META['HTTP_X_SIGNATURE'] = self.sig
        self.assertTrue(self.sig_mixin._test_signature(self.request))


class BasePermissionTestCase(BaseSignatureTestCase):
    def setUp(self):
        super().setUp()
        self.view = mock.Mock()
        self.request.user = mock.Mock()
        self.request.user.is_authenticated = lambda: False


class AlicePermissionTestCase(BasePermissionTestCase):

    def setUp(self):
        super().setUp()
        self.alice_perm = AlicePermission().has_permission

    def test_has_permission_schema_invalid_signature(self):
        self.view.action = 'schema'
        self.assertFalse(self.alice_perm(self.request, self.view))

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_has_permission_schema_valid_signature(self):
        self.view.action = 'schema'
        self.request.META['HTTP_X_SIGNATURE'] = self.sig
        self.assertTrue(self.alice_perm(self.request, self.view))

    def test_has_permission_nonschema_invalid_signature(self):
        self.assertFalse(self.alice_perm(self.request, self.view))

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_has_permission_nonschema_no_permission(self):
        self.request.META['HTTP_X_SIGNATURE'] = self.sig
        self.assertFalse(self.alice_perm(self.request, self.view))

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_has_permission_nonschema_valid_signature_and_permission(self):
        self.request.META['HTTP_X_SIGNATURE'] = self.sig
        self.request.user.is_authenticated = lambda: True
        self.assertTrue(self.alice_perm(self.request, self.view))


class SignatureOnlyAlicePermissionTestCase(BasePermissionTestCase):

    def setUp(self):
        super().setUp()
        self.sig_only_perm = SignatureOnlyAlicePermission().has_permission
        self.sig_only_obj_perm = (
            SignatureOnlyAlicePermission().has_object_permission
        )

    def test_has_permission_invalid_signature(self):
        self.assertFalse(self.sig_only_perm(self.request, self.view))

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_has_permission_valid_signature_no_permission(self):
        self.request.META['HTTP_X_SIGNATURE'] = self.sig
        self.assertTrue(self.sig_only_perm(self.request, self.view))

    def test_has_object_permission_invalid_signature(self):
        self.assertFalse(self.sig_only_obj_perm(self.request, self.view, None))

    @override_settings(UI_SECRET=AliceClient.SECRET)
    def test_has_object_permission_valid_signature_no_permission(self):
        self.request.META['HTTP_X_SIGNATURE'] = self.sig
        self.assertTrue(self.sig_only_obj_perm(self.request, self.view, None))
