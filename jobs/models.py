from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Jobs(models.Model):
     EXPERIENCE_CHOICES = [
        ('entry',  'Entry Level'),
        ('mid',    'Mid Level'),
        ('senior', 'Senior Level'),
    ]

     JOB_TYPE_CHOICES = [
        ('full_time',  'Full Time'),
        ('part_time',  'Part Time'),
        ('contract',   'Contract'),
        ('internship', 'Internship'),
        ('remote',     'Remote'),
    ]
     title = models.CharField(max_length=68)
     description = models.TextField()
     company_name = models.CharField(max_length=100)
     location = models.CharField(max_length=100,blank=True,null=True)
     experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES)
     salary=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
     job_type= models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
     skills=models.JSONField(default=list)
     posted_at =models.DateTimeField(auto_now_add=True)
     posted_by = models.ForeignKey(User,
                       on_delete = models.CASCADE,
                       related_name = 'jobs'
                   )
     deadline =models.DateTimeField(blank=True, null=True)

     class Meta:
          ordering = ['-posted_at']

     def __str__(self):
        return f'{self.title} at {self.company_name}' 
