from unittest import mock

from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.core.files import File
from parameterized import parameterized_class
from core.models import Item, Order, Coupon, UserProfile, Refund, OrderItem
from core.forms import PaymentForm, RefundForm, CouponForm
from core.views import OrderSummaryView, ItemDetailView, CheckoutView
from django.contrib.auth.models import User
from django.utils.text import slugify


# Models tests


class ItemModelTest(TestCase):
    def create_item(
            self,
            title="K-way",
            price=28.6,
            discount_price=5.1,
            category="SW",
            label="M",
            slug="",
            description="Hi",
            image="image.png",
    ):
        return Item.objects.create(
            title=title,
            price=price,
            discount_price=discount_price,
            category=category,
            label=label,
            slug=slug,
            description=description,
            image=image,
        )

    def test_item_creation(self):
        w = self.create_item()
        self.assertTrue(isinstance(w, Item))

        fields = (
            w.title,
            w.price,
            w.discount_price,
            w.category,
            w.label,
            w.slug,
            w.description,
            w.image,
        )
        self.assertEqual(w.__unicode__(), fields)


class CouponModelTest(TestCase):
    def create_coupon(
            self,
            code="13243abcd",
            amount=10.8
    ):
        return Coupon.objects.create(
            code=code,
            amount=amount,
        )

    def test_coupon_creation(self):
        w = self.create_coupon()
        self.assertTrue(isinstance(w, Coupon))

        fields = (
            w.code,
            w.amount
        )
        self.assertEqual(w.__unicode__(), fields)


# Forms tests


class PaymentFormTest(TestCase):
    def test_valid_form(self):
        data = {"stripeToken": "ciao", "save": "true", "use_default": "false"}
        form = PaymentForm(data=data)
        self.assertTrue(form.is_valid())


# Questo test se lasci la @ nell'email restituisce test
# corretto altrimenti restituisce errore nel test
class RefundFormTest(TestCase):
    def test_valid_form(self):
        data = {
            "ref_code": "234245",
            "message": "ciao",
            "email": "simone@mail.com",
        }
        form = RefundForm(data=data)
        self.assertTrue(form.is_valid())


class CouponFormTest(TestCase):
    def test_valid_form(self):
        data = {
            "code": "1234"
        }
        form = CouponForm(data=data)
        self.assertTrue(form.is_valid())


# Views tests


class TestViews(TestCase):

    def setup_view(view, request, *args, **kwargs):
        view.request = request
        view.args = args
        view.kwargs = kwargs
        return view


    # CheckoutView.get(self)

    def test_miao(self):
        factory = RequestFactory()
        request = factory.get('/order-summary')
        # v = setup_view(OrderSummaryView, request)
        # v.method_name()

    def test_AddCoupon(self):
        url = reverse("core:add-coupon")
        # resp = self.client.get(url)
        # self.assertEqual(resp.status_code, 405)  # Method not allowed

    def test_OrderSummary(self):
        url = reverse("core:order-summary")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)  # Redirect

    def test_OrderSummary2(self):
        response = self.client.get(reverse("core:order-summary"))
        self.assertEqual(response.status_code, 302)

    def test_Checkout(self):
        url = reverse("core:checkout")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)  # Redirect

    def test_get_orderSummary(self):
        # status_code = 200
        # view_class = OrderSummaryView

        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = OrderSummaryView.as_view()(req, *[], **{})
        self.assertEqual(resp.status_code, 302)

    def test_tryClient(self):
        c = Client()
        response = c.post('/checkout/')
        self.assertEqual(response.status_code, 302)  # Redirect
        response = c.post('/admin/')
        self.assertEqual(response.status_code, 302)

    # Parametrized tests


@parameterized_class(
    ("ref_code", "message", "email", "expected_result"),
    [
        ("141234", "ciao", "simone@gmail.com", True),  # giusta
        ("12345", "ciao", "simone.com", False),  # senza chiocciola
        ("32423", "ciao", "simone@gmail", False),
    ],
)  # senza punto
class RefundFormTestParametrized(TestCase):
    def test_form(self):
        data = {
            "ref_code": self.ref_code,
            "message": self.message,
            "email": self.email,
        }
        form = RefundForm(data=data)
        self.assertEqual(form.is_valid(), self.expected_result)


@parameterized_class(
    ("code", "amount", "expected_result"),
    [
        ("141234", 12.3, True),
        ("12345", 2.9, True),
        ("32423", 3.7, True),
    ],
)
class CouponFormTestParametrized(TestCase):
    def test_form(self):
        data = {
            "code": self.code,
            "amount": self.amount,
        }
        form = CouponForm(data=data)
        self.assertEqual(form.is_valid(), self.expected_result)

# Test con elementi come Mock

class RefundModelMock(TestCase):
    @mock.patch('core.models.Item', autospec=True)
    @mock.patch('core.models.Item.__str__', autospec=True)
    def test_mock(self,MockItem, MockItemMetodo):
        item= MockItem
        MockItemMetodo.return_value= "ciao"


# Test in cui l'immagine è mock
class ItemModelMockFile(TestCase):
    def create_item_image(
            self,
            image,
            title="K-way",
            price=28.6,
            discount_price=5.1,
            category="SW",
            label="M",
            slug="",
            description="Hi",
    ):
        file_mock = mock.MagicMock(spec=File)
        file_mock.name = image
        return Item.objects.create(
            title=title,
            price=price,
            discount_price=discount_price,
            category=category,
            label=label,
            slug=slug,
            description=description,
            image=file_mock,
        )

    def test_item_creation(self):
        w = self.create_item_image("image.png")
        self.assertTrue(isinstance(w, Item))

        fields = (
            w.title,
            w.price,
            w.discount_price,
            w.category,
            w.label,
            w.slug,
            w.description,
            w.image,
        )

        self.assertEqual(w.__unicode__(), fields)


if __name__ == '__main__':
    unittest.main()
