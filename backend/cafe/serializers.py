from rest_framework import serializers
from .models import Cafe, CafeEmployee

class CafeSerializer(serializers.ModelSerializer):
    employees = serializers.SerializerMethodField()
    
    class Meta:
        model = Cafe
        fields = ('name', 'description', 'employees', 'logo', 'location', 'id')
        
    def get_employees(self, obj):
        return CafeEmployee.objects.filter(cafe=obj).count()
        
