from datetime import date, timedelta

from django.forms import ValidationError
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from cafe.models import Cafe, CafeEmployee
from employee.models import Employee

class CafeTestCase(TestCase):
    def setUp(self):
        self.cafe = Cafe.objects.create(
            name="Cafe Latte",
            description="A cozy place",
            location="Uptown"
        )

    def test_cafe_creation(self):
        self.assertEqual(self.cafe.name, "Cafe Latte")
        self.assertEqual(self.cafe.location.location, "Uptown")
        self.assertEqual(Cafe.objects.count(), 1)

    def test_cafe_string_representation(self):
        self.assertEqual(str(self.cafe), "Cafe Latte")

class CafeAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cafe = Cafe.objects.create(
            name="Cafe Latte",
            description="A cozy place",
            location="Uptown"
        )
        self.cafe = Cafe.objects.create(
            name="Macchiato",
            description="We sell macchiato only",
            location="Uptown"
        )
        self.cafe = Cafe.objects.create(
            name="Amsterdam Coffee",
            description="Speciality Coffee Shop",
            location="Downtown"
        )
    
    def test_create_cafe(self):
        """
        Test  POST /cafes
        """
        response = self.client.post(reverse('cafe-list'), {
            "name": "Cafe Mocha",
            "description": "Another cozy place",
            "location": self.location.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cafe.objects.count(), 2)

    def test_filter_cafes_by_location(self):
        """
        Test  Get /cafes?location=<valid location>
        """
        url = reverse('cafes-list')  # 'cafes-list' corresponds to the list action of the CafeViewSet
        response = self.client.get(url, {'location': 'Downtown'})


        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(len(response_data), 2)
        for cafe in response_data:
            self.assertEqual(cafe['location'], 'Downtown')

    def test_no_cafes_for_nonexistent_location(self):
        """
        Get /cafes?location=<invalid location>
        """
        url = reverse('cafes-list')
        response = self.client.get(url, {'location': 'Nonexistent'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(len(response_data), 0)  # No cafes should be returned

    def test_all_cafes_returned_without_location_filter(self):
        """
        Get /cafes
        """
        url = reverse('cafes-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(len(response_data), 3)
        
class CafeEmployeeTestCase(TestCase):
    def setUp(self):
        # Set up any initial data or test objects here if necessary
        self.valid_start_date = date.today() - timedelta(days=30)  # 30 days ago
        self.future_start_date = date.today() + timedelta(days=1)  # 1 day in the future

    def test_valid_start_date(self):
        # Create a CafeEmployee with a valid start_date (today or before today)
        cafe_employee = CafeEmployee(start_date=self.valid_start_date)
        try:
            cafe_employee.full_clean()  # Validates the instance
            cafe_employee.save()  # Saves if no validation errors
        except ValidationError:
            self.fail("CafeEmployee with a valid start_date raised ValidationError")

    def test_future_start_date_raises_error(self):
        # Attempt to create a CafeEmployee with a future start_date
        cafe_employee = CafeEmployee(start_date=self.future_start_date)
        with self.assertRaises(ValidationError):
            cafe_employee.full_clean()  # This should raise a ValidationError

    def test_start_date_today(self):
        # Create a CafeEmployee with today's start_date
        cafe_employee = CafeEmployee(start_date=date.today())
        try:
            cafe_employee.full_clean()  # Validates the instance
            cafe_employee.save()  # Saves if no validation errors
        except ValidationError:
            self.fail("CafeEmployee with today's start_date raised ValidationError")
            
class EmployeeSortTestCase(TestCase):
    def setUp(self):
        # Create CafeEmployee instances with different start dates
        cafe_employee1 = CafeEmployee.objects.create(start_date=date.today() - timedelta(days=10))  # 10 days ago
        cafe_employee2 = CafeEmployee.objects.create(start_date=date.today() - timedelta(days=20))  # 20 days ago
        cafe_employee3 = CafeEmployee.objects.create(start_date=date.today() - timedelta(days=5))   # 5 days ago

        # Create Employee instances linked to the CafeEmployee instances
        self.employee1 = Employee.objects.create(name="John Doe", cafe_employee=cafe_employee1)
        self.employee2 = Employee.objects.create(name="Jane Doe", cafe_employee=cafe_employee2)
        self.employee3 = Employee.objects.create(name="Jim Doe", cafe_employee=cafe_employee3)

    def test_sort_employees_by_start_date(self):
        # Define the URL for the employees endpoint (use the appropriate name for your URL)
        url = reverse('employees-list')  # Replace 'employees-list' with the actual name in your urls.py

        # Make a GET request to the API
        response = self.client.get(url, {'ordering': 'cafeemployee__start_date'})  # Ascending order by start_date

        # Ensure the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Extract the employee IDs from the sorted response data
        response_data = response.json()
        employee_ids = [employee['id'] for employee in response_data]

        # Verify the order is by ascending start_date
        expected_order = [self.employee2.id, self.employee1.id, self.employee3.id] #20 days, 10days, 5 days
        self.assertEqual(employee_ids, expected_order)
