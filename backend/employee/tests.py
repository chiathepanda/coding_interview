import re

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from employee.models import Employee,  generate_id

employee_path = '/employee'
employees_path = '/employees'

class EmployeeAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.employee_data = {
            "name": "Alice Smith",
            "email_address": "alice@example.com",
            "phone_number": "81234567",
            "gender": "female"
        }

    def test_get_all_employees(self):
        response = self.client.get(reverse('employee-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_employee(self):
        """
        Test  POST /employee
        """
        url = reverse('employee-api')
        self.assertEqual(url, employee_path)
        current_count = Employee.objects.count()
        response = self.client.post(reverse('employee-api'), self.employee_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), current_count + 1)
        
    def test_update_employee(self):
        """
        Test  PUT /employee
        """
        url = reverse('employee-api')
        self.assertEqual(url, employee_path)
        self.client.post(reverse('employee-api'), self.employee_data)
        employee_id = Employee.objects.all().first().id
        NewName = "New Name"
        NewEmailAddress = "test@example.com"
        NewPhoneNumber = "90000000"
        response = self.client.put(url, {
            "id": employee_id,
            "name": NewName,
            "gender": "male",
            "email_address": NewEmailAddress,
            "phone_number": NewPhoneNumber
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], NewName)
        self.assertEqual(response.data['email_address'], NewEmailAddress)
        self.assertEqual(response.data['phone_number'], NewPhoneNumber)

    def test_delete_employee(self):
        """
        Test  DELETE /employee
        """
        url = reverse('employee-api')
        self.assertEqual(url, employee_path)
        self.client.post(reverse('employee-api'), self.employee_data)
        employees = Employee.objects.all()
        current_len = len(employees)
        employee_id = Employee.objects.all().first().id
        response = self.client.delete(url,
                                      {"id": employee_id
                                       })
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(Employee.objects.all()), current_len-1)