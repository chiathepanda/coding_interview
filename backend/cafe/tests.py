from datetime import date, timedelta

from django.forms import ValidationError
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from cafe.models import Cafe, CafeEmployee
from employee.models import Employee

cafe_path = '/cafe'
cafes_path = '/cafes'

class CafeAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cafe = Cafe.objects.create(
            name="Cafe Latte",
            description="A cozy place",
            location="UPTOWN"
        )
        self.cafe = Cafe.objects.create(
            name="Macchiato",
            description="We sell macchiato only",
            location="UPTOWN"
        )
        self.cafe = Cafe.objects.create(
            name="Amsterdam Coffee",
            description="Speciality Coffee Shop",
            location="DOWNTOWN"
        )
        
    def test_filter_cafes_by_location(self):
        """
        Test  Get /cafes?location=<valid location>
        """
        url = reverse('cafe-list')
        self.assertEqual(url, cafes_path)
        response = self.client.get(url, {'location': 'Downtown'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(len(response_data), 1)
        for cafe in response_data:
            self.assertEqual(cafe['location'], 'DOWNTOWN')

    def test_no_cafes_for_nonexistent_location(self):
        """
        Get /cafes?location=<invalid location>
        """
        url = reverse('cafe-list')
        response = self.client.get(url, {'location': 'Nonexistent'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(len(response_data), 0)  # No cafes should be returned

    def test_all_cafes_returned_without_location_filter(self):
        """
        Get /cafes
        """
        url = reverse('cafe-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(len(response_data), 3)
        
    def test_create_cafe(self):
        """
        Test  POST /cafe
        """
        url = reverse('cafe-api')
        self.assertEqual(url, cafe_path)
        response = self.client.post(url, {
            "name": "Cafe Mocha",
            "description": "Another cozy place",
            "location": "BISHAN"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cafe.objects.count(), 4)
        
    def test_update_cafe(self):
        """
        Test  PUT /cafe
        """
        url = reverse('cafe-api')
        self.assertEqual(url, cafe_path)
        cafe_id = Cafe.objects.all().first().id
        NewName = "New Name"
        NewDescription = "New Description"
        NewLocation = "NEW LOCATION"
        response = self.client.put(url, {
            "id": cafe_id,
            "name": NewName,
            "description": NewDescription,
            "location": NewLocation
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], NewName)
        self.assertEqual(response.data['description'], NewDescription)
        self.assertEqual(response.data['location'], NewLocation)

    def test_delete_cafe(self):
        """
        Test  DELETE /cafe
        """
        url = reverse('cafe-api')
        self.assertEqual(url, cafe_path)
        cafes = Cafe.objects.all()
        current_len = len(cafes)
        cafe_id = Cafe.objects.all().first().id
        response = self.client.delete(url,
                                      {"id": cafe_id
                                       })
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(Cafe.objects.all()), current_len-1)
        
class CafeEmployeeTestCase(TestCase):
    def setUp(self):
        # Set up any initial data or test objects here if necessary
        self.valid_start_date = date.today() - timedelta(days=30)  # 30 days ago
        self.future_start_date = date.today() + timedelta(days=1)  # 1 day in the future

            
class EmployeeSortTestCase(TestCase):
    def setUp(self):
        self.cafe = Cafe.objects.create(
            name="Cafe Latte",
            description="A cozy place",
            location="UPTOWN"
        )
        
        # Create Employee instances linked to the CafeEmployee instances
        self.employee1 = Employee.objects.create(name="John Doe")
        self.employee2 = Employee.objects.create(name="Jane Doe")
        self.employee3 = Employee.objects.create(name="Jim Doe")
        
        # Create CafeEmployee instances with different start dates
        CafeEmployee.objects.create(
            cafe_id=self.cafe.id,
            employee=self.employee1,
            start_date=date.today() - timedelta(days=10))  # 10 days ago
        CafeEmployee.objects.create(
            cafe_id=self.cafe.id, 
            employee=self.employee2,
            start_date=date.today() - timedelta(days=20))  # 20 days ago
        CafeEmployee.objects.create(
            cafe_id=self.cafe.id,
            employee=self.employee3,
            start_date=date.today() - timedelta(days=5))   # 5 days ago

    def test_sort_employees_by_start_date(self):
        # Define the URL for the employees endpoint (use the appropriate name for your URL)
        url = reverse('employee-list')  # Replace 'employees-api' with the actual name in your urls.py

        # Make a GET request to the API
        response = self.client.get(url)  # Ascending order by start_date

        # Ensure the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Extract the employee IDs from the sorted response data
        response_data = response.json()
        employee_ids = [employee['id'] for employee in response_data]

        # Verify the order is by ascending start_date
        expected_order = [self.employee2.id, self.employee1.id, self.employee3.id] #20 days, 10days, 5 days
        self.assertEqual(employee_ids, expected_order)
