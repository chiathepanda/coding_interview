import re

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from employee.models import Employee

class EmployeeTestCase(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            id=Employee.generate_id(),
            name="Jane Doe",
            email_address="jane.doe@example.com",
            phone_number="81234567",
            gender="female"
        )

    def test_employee_creation(self):
        self.assertEqual(self.employee.name, "Jane Doe")
        self.assertTrue(re.match(r'^UI[A-Z0-9]{7}$', self.employee.id))
        self.assertEqual(Employee.objects.count(), 1)

    def test_employee_phone_number_validation(self):
        with self.assertRaises(ValidationError):
            Employee.objects.create(
                id=Employee.generate_id(),
                name="Invalid Phone",
                email_address="invalid.phone@example.com",
                phone_number="71234567",  # Invalid because it does not start with 8 or 9
                gender="female"
            )

    def test_generate_id(self):
        generated_id = Employee.generate_id()
        self.assertTrue(re.match(r'^UI[A-Z0-9]{7}$', generated_id))

class EmployeeAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.employee_data = {
            "id": Employee.generate_id(),
            "name": "Alice Smith",
            "email_address": "alice@example.com",
            "phone_number": "81234567",
            "gender": "female"
        }

    def test_get_all_employees(self):
        response = self.client.get(reverse('employee-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_employee(self):
        response = self.client.post(reverse('employee-list'), self.employee_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 1)
