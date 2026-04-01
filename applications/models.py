# applications/models.py
from django.db import models
from django.conf import settings

class Application(models.Model):
    job          = models.ForeignKey('jobs.Jobs', on_delete=models.CASCADE)
    applicant    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resume       = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True)
    match_score  = models.FloatField(default=0.0)
    status       = models.CharField(max_length=20, choices=[
        ('applied',     'Applied'),
        ('shortlisted',   'Shortlisted'),
        ('assessment',  'Assessment'),
        ('interview',   'Interview'),
        ('offer',       'Offer'),
        ('hired',       'Hired'),
        ('rejected',    'Rejected'),
    ], default='applied')
    applied_at   = models.DateTimeField(auto_now_add=True)

class ParsedResume(models.Model):
    application  = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='parsed')
    name         = models.CharField(max_length=100, blank=True)
    email        = models.EmailField(blank=True)
    phone        = models.CharField(max_length=20, blank=True)
    skills       = models.JSONField(default=list)        # ['python', 'django', 'react']
    experience   = models.JSONField(default=list)        # list of experience dicts
    education    = models.JSONField(default=list)        # list of education dicts
    raw_text     = models.TextField(blank=True)          # full extracted text
    parsed_at    = models.DateTimeField(auto_now_add=True)
    location     = models.CharField(max_length=100,blank=True)
