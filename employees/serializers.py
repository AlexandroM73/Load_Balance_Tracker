from rest_framework import serializers

from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "full_name", "position", "email", "is_active", "created_at"]
        read_only_fields = ["id", "created_at"]
