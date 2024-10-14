from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('employee', EmployeeViewSet.as_view(
        {
            'post': 'create_employee',
            'put': 'update_employee',
            'delete': 'delete_employee'
         }), name='employee-api'),
] 