from django.db import IntegrityError, transaction
from django.db.models import F
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from cafe.models import Cafe, CafeEmployee
from .models import Employee
from .serializers import EmployeeSerializer

class EmployeeViewSet(viewsets.ViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    
    def list(self, request):
        location_name = request.GET.get('location')
        cafe_id = request.GET.get('cafe_id')
        
        if location_name or cafe_id:
            if location_name:
                employees = Employee.objects.filter(location__location__icontains=location_name)
            if cafe_id:
                employees = Employee.objects.filter(cafeemployee__cafe_id=cafe_id)
        else:
            employees = Employee.objects.all()
        
        employees = employees.order_by(
            F('cafeemployee__start_date').asc(nulls_last=True)
            )
        
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)
    
    # POST /employee
    @action(detail=False, methods=['post'])
    def create_employee(self, request):
        try: 
            with transaction.atomic():
            
                serializer = EmployeeSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                employee = serializer.save()
                
                cafe_relation = request.data.get('cafe_relation')
                
                if cafe_relation:
                    cafe_id = cafe_relation.get('cafe_id')
                    start_date = cafe_relation.get('start_date')
                    
                    cafe_id = None if cafe_id == "" else cafe_id
                    start_date = None if start_date == "" else start_date
                    
                    if cafe_id is not None and start_date is None:
                        raise ValueError("Cafe must be provided since 'start_date' was provided in 'cafe_relation'.")

                    filtered = Cafe.objects.filter(id=cafe_id)
                        
                    if cafe_id is not None and not filtered.exists():
                        raise ValueError("The specified 'cafe_id' does not exist.")
                    
                    if len(filtered) > 0:
                        CafeEmployee.objects.update_or_create(
                            employee=employee,
                            defaults={'cafe_id': cafe_id,
                                    "start_date": start_date}
                        )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


    # PUT /employee
    @action(detail=False, methods=['put'])
    def update_employee(self, request):
        try:
            with transaction.atomic():
                employee_id = request.data.get('id')
                cafe_relation = request.data.get('cafe_relation')
                cafe_relation = None if cafe_relation == "" else cafe_relation
                cafe_id = None
                if cafe_relation:
                    cafe_id = cafe_relation['cafe_id']
                    start_date = cafe_relation['start_date']
                    
                    cafe_id = None if cafe_id == "" else cafe_id
                    start_date = None if start_date == "" else start_date

                if not employee_id:
                    return Response(
                        {"error": "Employee ID as 'id' is required."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                try:
                    employee = Employee.objects.get(id=employee_id)
                except Employee.DoesNotExist:
                    return Response(
                        {"error": "Employee not found."},
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                serializer = EmployeeSerializer(employee, data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    
                # Handle the cafe relation, use first() since it's unique to employee
                existing_relation = CafeEmployee.objects.filter(employee=employee).first()
                if not cafe_relation and existing_relation is not None:
                    # If no cafe relation is provided, remove the existing relation if it exists
                    existing_relation.delete()
                elif cafe_relation is not None and not Cafe.objects.filter(id=cafe_id).exists():
                    return Response({"error": "The specified cafe_id does not exist."}, status=status.HTTP_400_BAD_REQUEST)
                elif cafe_relation is not None and not existing_relation or \
                (existing_relation is not None and \
                 (cafe_id != getattr(existing_relation, 'cafe_id') or \
                    start_date != getattr(existing_relation, 'start_date'))):
                    CafeEmployee.objects.update_or_create(
                        employee=employee,  # Lookup field
                        defaults={
                            'cafe_id': cafe_id,
                            'start_date': start_date
                        }
                    )
                    
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # DELETE /employee
    @action(detail=False, methods=['delete'])
    def delete_employee(self, request):
        try:
            with transaction.atomic():
                delete_id = request.data if type(request.data) == str else request.data.get('id', None)
                employee = get_object_or_404(Employee, pk=delete_id)

                employee.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        except IntegrityError as e:
                # e.g. foreign key constraints
                return Response(
                    {"error": "Unable to delete employee due to related objects. Please resolve dependencies before deleting."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
                return Response(
                    {"error": f"Failed to delete employee: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )