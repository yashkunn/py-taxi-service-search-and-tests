from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.models import Car, Manufacturer
from taxi.forms import (
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm,
    DriverCreationForm)


class FormTest(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "test",
            "password1": "Str0ngP@ssw0rd!",
            "password2": "Str0ngP@ssw0rd!",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "UNI12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def driver_license_update_form(self):
        form_data = {
            "license_number": "NEW12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form_invalid(self):
        form_data = {
            "license_number": "NEW"
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class TestSearchForms(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="testdriver",
            password="testpass123",
            first_name="Test",
            last_name="Driver",
            license_number="UNI12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.car = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer
        )

    def test_driver_search_form(self):
        form_data = {"username": "testdriver"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        drivers = get_user_model().objects.filter(
            username__icontains=form_data["username"]
        )
        self.assertEqual(list(drivers), [self.driver])

    def test_car_search_form(self):
        form_data = {"model": "Test Model"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        cars = Car.objects.filter(model__icontains=form_data["model"])
        self.assertEqual(list(cars), [self.car])

    def test_manufacturer_search_form(self):
        form_data = {"name": "Test Manufacturer"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        manufacturers = Manufacturer.objects.filter(
            name__icontains=form_data["name"]
        )
        self.assertEqual(list(manufacturers), [self.manufacturer])
