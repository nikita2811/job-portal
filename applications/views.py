from django.shortcuts import render
# applications/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsApplicant, IsHR, IsHROrManager
from .models import Application
from .serializers import ApplicationSerializer
from .tasks import send_application_email
class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsApplicant()]                      # only applicants can apply
        if self.action in ['list', 'retrieve', 'parsed_data']:
            return [IsHROrManager()]                    # HR/Manager can view
        return [IsHR()]                                 # HR for everything else

    def get_queryset(self):
        user = self.request.user
        if user.role == 'applicant':
            return Application.objects.filter(applicant=user)
        return Application.objects.all().order_by('-match_score') # HR sees ranked list

    def perform_create(self, serializer):
        data = serializer.save(applicant=self.request.user)
        send_application_email.delay(data)
        

    @action(detail=True, methods=['get'], url_path='parsed-data')
    def parsed_data(self):
        """HR can view parsed resume data."""
        application = self.get_object()
        return Response({
            'match_score': application.match_score,
            'parsed':      {
                'name':       application.parsed.name,
                'email':      application.parsed.email,
                'skills':     application.parsed.skills,
                'experience': application.parsed.experience,
                'education':  application.parsed.education,
            }
        })

    @action(detail=True, methods=['patch'], url_path='move-stage', permission_classes=[IsHROrManager])
    def move_stage(self, request,):
        """Move application to next pipeline stage."""
        application        = self.get_object()
        new_stage          = request.data.get('status')
        application.status = new_stage
        application.save()
        return Response({'detail': f'Moved to {new_stage}'})