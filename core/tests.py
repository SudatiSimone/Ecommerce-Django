import unittest

from unittest import mock
from django.test import LiveServerTestCase
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify
from core.models import *
from core.forms import *
from core.views import *
from core.urls import *
from unittest.mock import MagicMock
from django.core.files import File
from parameterized import parameterized, parameterized_class
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

"""
Models tests
"""


class ItemModelTest(TestCase):
    def create_item(self, title="K-way", price=28.6, discount_price=5.1, category='SW', label='M', slug="",
                    description="Hi", image="image.png"):
        return Item.objects.create(title=title, price=price, discount_price=discount_price, category=category,
                                   label=label,
                                   slug=slug, description=description, image=image)

    def test_item_creation(self):
        w = self.create_item()
        self.assertTrue(isinstance(w, Item))

        fields = w.title, w.price, w.discount_price, w.category, w.label, w.slug, w.description, w.image
        self.assertEqual(w.__unicode__(), fields)


"""
Forms tests
"""


class PaymentFormTest(TestCase):
    def test_valid_form(self):
        data = {'stripeToken': "ciao", 'save': 'true', 'use_default': 'false'}
        form = PaymentForm(data=data)
        self.assertTrue(form.is_valid())


# Questo test se lasci la @ nell'email restituisce test corretto altrimenti restituisce errore nel test
class RefundFormTest(TestCase):
    def test_valid_form(self):
        data = {'ref_code': '234245', 'message': 'ciao', 'email': 'simone@mail.com'}
        form = RefundForm(data=data)
        self.assertTrue(form.is_valid())


"""
Views tests
"""


class ViewTest(TestCase):
    def test_AddCoupon(self):
        url = reverse('core:add-coupon')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 405)  # Method not allowed

    def test_OrderSummary(self):
        url = reverse('core:order-summary')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)  # Redirect

    def test_Checkout(self):
        url = reverse('core:checkout')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)  # Redirect


"""
    def test_Product(self):
        url = reverse('core:product')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)  # Redirect
"""

"""
Parametrized tests
"""


@parameterized_class(
    ("ref_code", "message", "email", "expected_result"), [
        ("141234", "ciao", "simone@gmail.com", True),  # giusta
        ("12345", "ciao", "simone.com", False),  # senza chiocciola
        ("32423", "ciao", "simone@gmail", False), ], )  # senza punto
class RefundFormTestParametrized(TestCase):
    def test_form(self):
        data = {'ref_code': self.ref_code, 'message': self.message,
                'email': self.email, }
        form = RefundForm(data=data)
        self.assertEqual(form.is_valid(), self.expected_result)


""""
Test con elementi come Mock 
"""


class AddCouponViewMock(TestCase):

    @mock.patch('core.views.get_coupon')
    def AddCouponMock(self, mock_get_coupon):
        # code = "321"
        # amount = 20

        order = Order.objects.create(user=self.request.user, ordered=False)
        order.coupon = mock_get_coupon
        order.save()
        self.assertIn(order.coupon, Coupon)


# Test in cui l'immagine è mock
class ItemModelMockFile(TestCase):

    def create_item_image(self, image, title="K-way", price=28.6, discount_price=5.1, category='SW', label='M', slug="",
                          description="Hi"):
        file_mock = mock.MagicMock(spec=File)
        file_mock.name = image
        return Item.objects.create(title=title, price=price, discount_price=discount_price, category=category,
                                   label=label, slug=slug, description=description, image=file_mock)

    def test_item_creation(self):
        w = self.create_item_image("image.png")
        self.assertTrue(isinstance(w, Item))

        fields = w.title, w.price, w.discount_price, w.category, w.label, w.slug, w.description, w.image
        self.assertEqual(w.__unicode__(), fields)




""""

def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("core:checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("core:checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("core:checkout")

"""
