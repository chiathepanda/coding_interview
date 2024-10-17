from datetime import date, datetime
from rest_framework import serializers
from cafe.models import CafeEmployee
from .models import Employee

class CafeEmployeeSerializer(serializers.ModelSerializer):
    cafe_id = serializers.UUIDField() 
    start_date = serializers.DateField(format="%Y-%m-%d") # i.e. YYYY-MM-DD

    class Meta:
        model = CafeEmployee
        fields = ['cafe_id', 'start_date']
        
        
class EmployeeSerializer(serializers.ModelSerializer):
    cafe_relation = serializers.SerializerMethodField()
    days_worked = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ('id', 'name', 'email_address', 'phone_number', 'days_worked', 'gender', 'cafe_relation')

    def get_cafe_relation(self, obj):
        try:
            # Attempt to fetch the related Cafe through the CafeEmployee relationship.
            cafe_employee = CafeEmployee.objects.get(employee=obj)
            return {
                'cafe_id': cafe_employee.cafe.id,
                'name': cafe_employee.cafe.name,
                'start_date': cafe_employee.start_date
            }
        except CafeEmployee.DoesNotExist:
            return {
                'cafe_id': None,
                'name': None,
                'start_date': None
            }
        
    def get_days_worked(self, obj):
        if hasattr(obj, 'cafeemployee'):
            start_date = obj.cafeemployee.start_date
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            return (date.today() - start_date).days
        