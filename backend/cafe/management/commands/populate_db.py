from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import connection

from backend.settings import DATABASES
from cafe.models import Cafe, CafeEmployee
from employee.models import Employee

class Command(BaseCommand):
    help = "Populate db astekproject with dummy data"

    # omit add arguments
    def handle(self, *args, **options):
        try:
            with connection.cursor() as cursor:
                required_tables = set(['cafe_cafe', 'cafe_cafeemployee', 'employee_employee'])
                tables = connection.introspection.table_names(cursor)
                missing = (required_tables - set(tables))
                
                if missing: 
                    self.stdout.write(self.style.ERROR(f"One of the Table '{required_tables}' does not exist. Please check your database astekproject and use django's makemigrations and migrate first. For more instructions, read READ.ME"))

                if len(missing) == 0 and not Cafe.objects.exists() and not Employee.objects.exists() and not CafeEmployee.objects.exists():

                    cafes = [
                        Cafe.objects.create(
                            name="First Cafe Latte",
                            description="A cozy place for latte lovers",
                            location="Uptown"
                        ),
                        Cafe.objects.create(
                            name="Macchiato House",
                            description="We specialize in macchiato",
                            location="Uptown"
                        ),
                        Cafe.objects.create(
                            name="Amsterdam Coffee",
                            description="Specialty coffee shop in the heart of Downtown",
                            location="Downtown"
                        ),
                        Cafe.objects.create(
                            name="Sunrise Espresso",
                            description="Start your day with a strong espresso",
                            location="Midtown"
                        ),
                        Cafe.objects.create(
                            name="Brewed Bliss",
                            description="Your daily dose of happiness",
                            location="Uptown"
                        ),
                        Cafe.objects.create(
                            name="Cappuccino Corner",
                            description="Cappuccinos served with a smile",
                            location="Suburbs"
                        ),
                        Cafe.objects.create(
                            name="Mocha Madness",
                            description="For the chocolate and coffee lovers",
                            location="Downtown"
                        ),
                        Cafe.objects.create(
                            name="Vintage Beans",
                            description="A rustic spot with a vintage charm",
                            location="Old Town"
                        )
                    ]
                    self.stdout.write(self.style.SUCCESS(f"Successfully created {len(cafes)} cafes."))
                    employees = [
                        Employee.objects.create(
                            name="Grandma",
                            email_address="grandma@example.com",
                            phone_number="81234001",
                            gender="female"
                            ),
                        Employee.objects.create(
                            name="Jane Doe",
                            email_address="jane.doe@example.com",
                            phone_number="81234002",
                            gender="female"
                            ),
                        Employee.objects.create(
                            name="Jenson Hao",
                            email_address="Jenson.hao@gmail.com",
                            phone_number="81234009",
                            gender="male"
                            )
                    ]
                    self.stdout.write(self.style.SUCCESS(f"Successfully created {len(employees)} employees."))

                    CafeEmployee.objects.create(
                        employee = employees[0],
                        cafe = cafes[0],
                        start_date=date.today() - timedelta(days=365))
                    
                    CafeEmployee.objects.create(
                        employee = employees[1],
                        cafe = cafes[0],
                        start_date=date.today() - timedelta(days=10),
                    )

                    CafeEmployee.objects.create(
                        employee = employees[2],
                        cafe = cafes[1],
                        start_date=date.today() - timedelta(days=10),
                    )
                    
                    self.stdout.write(self.style.SUCCESS(f"Successfully created relation cafe employees."))
                    self.stdout.write(self.style.SUCCESS(f"Successfully created dummy data."))
                else:
                    self.stdout.write(self.style.NOTICE("Data already filled. Thus, it was not autopopulated."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))