from rest_framework import serializers
from .models import Jobs

class JobSerializer(serializers.ModelSerializer):
    posted_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Jobs
        fields = [
            'id', 'title', 'description', 'company_name',
            'location', 'experience', 'salary', 'job_type',
            'skills', 'posted_at', 'posted_by', 'deadline'
        ]
        read_only_fields = ['id', 'posted_at', 'posted_by']


class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = [
            'title', 'description', 'company_name',
            'location', 'experience', 'salary', 'job_type',
            'skills', 'deadline'
        ]

    def validate_skills(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Skills must be a list.")
        if len(value) == 0:
            raise serializers.ValidationError("At least one skill is required.")
        return value
    
    def validate_salary(self, value):
        if value and value < 0:
            raise serializers.ValidationError("Salary cannot be negative.")
        return value