from datetime import date
import uuid

from django.db import models
from django.forms import ValidationError

from backend.models import TimeStampMixin
from employee.models import Employee
    
class Cafe(TimeStampMixin):
    id = models.UUIDField(null=False, blank=False, primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(null=False, blank=False, max_length=255)
    description = models.CharField(null=False, blank=False, max_length=256)
    logo = models.ImageField(upload_to='img/cafe_logos/', null=True, blank=True)
    location = models.CharField(null=False, blank=False, max_length=255)
    
    def __str__(self):
        return f"{self.name} {self.location}, {self.id}"
    
    class Meta:
        abstract = False

class CafeEmployee(TimeStampMixin):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    start_date = models.DateField(null=False, blank=False)

    def clean(self):
        # Otherwise, need to handle days_worked (it will be negative if this is in the future)
        if self.start_date > date.today():
            raise ValidationError("Start date cannot be in the future.")
        
    class Meta:
        unique_together = ('employee', 'cafe')