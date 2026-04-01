# applications/serializers.py
from rest_framework import serializers
from .models import Application, ParsedResume

class ParsedResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ParsedResume
        fields = ['name', 'email', 'phone', 'skills', 'experience', 'education']

class ApplicationSerializer(serializers.ModelSerializer):
    parsed = ParsedResumeSerializer(read_only=True)

    class Meta:
        model  = Application
        fields = ['id', 'job', 'resume', 'cover_letter',
                  'status', 'match_score', 'parsed', 'applied_at']
        read_only_fields = ['status', 'match_score']