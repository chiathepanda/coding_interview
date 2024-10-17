from django.core.files.storage import default_storage
from django.db import IntegrityError
from django.db.models import Count
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from .models import Cafe
from .models import Employee
from .serializers import CafeSerializer

class CafeViewSet(viewsets.ViewSet):
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    def list(self, request):
        location_name = request.GET.get('location')
        if location_name:
            cafes = Cafe.objects.filter(location__icontains=location_name)
        else:
            cafes = Cafe.objects.all()
        
        cafes = cafes.annotate(employees=Count('cafeemployee'))
        
        serializer = CafeSerializer(cafes.order_by('-employees'), many=True)
        return Response(serializer.data)

    # POST /cafe
    @action(detail=False, methods=['post'])
    def create_cafe(self, request):
        serializer = CafeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT /cafe
    @action(detail=False, methods=['put'])
    def update_cafe(self, request, pk=None):
        try: 
            data = request.data.copy()
            cafe_id = request.data.get('id')
            cafe_logo = request.data.get('logo')
            if not cafe_id:
                return Response({'error': 'Cafe ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
                
            cafe = get_object_or_404(Cafe, pk=cafe_id)
            
            # If a logo already exists, delete the image file from storage
            if not cafe_logo and cafe.logo:
                logo_path = cafe.logo.path
                if default_storage.exists(logo_path):
                    default_storage.delete(logo_path)
                data['logo'] = None
            
            serializer = CafeSerializer(cafe, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE /cafe 
    @action(detail=False, methods=['delete'])
    def delete_cafe(self, request, pk=None):
        cafe_id = request.data if type(request.data) == str else request.data.get('id')
        if not cafe_id:
            return Response({'error': 'Cafe ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cafe = get_object_or_404(Cafe, pk=cafe_id)
       
            cafe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except IntegrityError as e:
            return Response(
                {"error": "Unable to delete cafe due to related objects. Please resolve dependencies before deleting."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to delete cafe: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )








