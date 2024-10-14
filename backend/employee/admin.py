from django.contrib import admin
from cafe.models import CafeEmployee, Cafe
from .models import Employee

class CafeEmployeeInline(admin.StackedInline):
    model = CafeEmployee
    extra = 1  # extra entry
    autocomplete_fields = ['cafe'] 
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "cafe":
            kwargs["queryset"] = Cafe.objects.all()  # You can filter the cafes here if needed.
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    inlines = [CafeEmployeeInline]
    search_fields = ('name', 'email_address', 'phone_number')
    readonly_fields = ['id']
    
    def save_model(self, request, obj, form, change):
        # Save the parent before the child
        if not obj.id:
            obj.save()
        super().save_model(request, obj, form, change)
    

