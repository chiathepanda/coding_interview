import random
import string

from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator

from backend.models import UpperCaseCharField, TimeStampMixin

employeeIDValidator = RegexValidator(r'^(UI)([A-Za-z0-9]{7})$', 'Begins with 6 alphabets and Ends with =X')
phoneNumberValidator = RegexValidator(r'^[89][0-9]{7}$', 'The Phone Number must start with either 8 or 9 and must have 8 digits in total.')

def generate_id():
    # generate format 'UIXXXXXXX' where the X is alphanumeric
    prefix = 'UI'
    
    while True:
        suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
        new_id = f'{prefix}{suffix}'
        if not Employee.objects.filter(id=new_id).exists():
            return new_id
            
class Employee(TimeStampMixin):
    # customo id of format 'UIXXXXXXX' where X is alphanumeric
    id = UpperCaseCharField(null=False, blank=False, unique=True, max_length=10, primary_key=True, default=generate_id, validators=[employeeIDValidator])
    name = models.CharField(null=False, blank=False, max_length=255)
    email_address = models.EmailField(null=False, blank=False)
    phone_number = models.CharField(null=False, blank=False, max_length=8, validators=[phoneNumberValidator, MinLengthValidator(8), MaxLengthValidator(8)])
    gender = models.CharField(null=False, blank=False, max_length=6, choices=[('male', 'Male'), ('female', 'Female')])
    
    class Meta:
        abstract = False
    
    def save(self, *args, **kwargs):
        # If the object doesn't have an ID yet
        if not self.id:
            self.id = self.generate_id()
        super().save(*args, **kwargs)