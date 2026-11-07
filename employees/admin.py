from django.contrib import admin

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "position", "email", "is_active")
    list_filter = ("position", "is_active")
    search_fields = ("full_name", "email")
