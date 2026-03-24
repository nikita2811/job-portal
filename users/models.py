from django.db import models
from django.contrib.auth.models import (BaseUserManager,AbstractBaseUser,PermissionsMixin)
from django.utils import timezone
import uuid
from django.conf import settings

# Create your models here.
class UserManager(BaseUserManager):

 def create_user(self,email,password=None,**extra_fields):
  
  if not email:
   raise TypeError('User must have email')
  
  user = self.model(email=self.normalize_email(email),**extra_fields)
  if password:
   user.set_password(password)
  user.save()

  return user
 
 def create_superuser(self,email,password,**extra_fields):
  user = self.create_user(email,password,**extra_fields)
  user.is_active = True
  user.superuser = True
  user.is_verified = True

  user.save()

  return user


class User(AbstractBaseUser,PermissionsMixin):
 
 class Role(models.TextChoices):
        HR = 'hr', 'HR'
        MANAGER = 'manager', 'Manager'
        TEAM = 'team_member', 'Team Member'
        APPLICANT = 'applicant', 'Applicant'
 name = models.CharField(max_length=68)
 email = models.EmailField(max_length=255,unique=True,db_index=True)
 is_verified = models.BooleanField(default=False)
 is_active =models.BooleanField(default=False)
 is_staff=models.BooleanField(default=False)
 role=models.CharField(max_length=20,choices=Role.choices, default=Role.APPLICANT)

 USERNAME_FIELD='email'

 objects = UserManager()

 def is_hr(self):
        return self.role == self.Role.HR

 def is_manager(self):
     return self.role == self.Role.MANAGER
 
 def is_team(self):
     return self.role == self.Role.TEAM 
 
 def is_applicant(self):
        return self.role == self.Role.APPLICANT

 def __str__(self):
  return self.email
 

class TeamInvite(models.Model):
    class Status(models.TextChoices):
        PENDING  = 'pending',  'Pending'
        ACCEPTED = 'accepted', 'Accepted'
        EXPIRED  = 'expired',  'Expired'
    token      = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    email      = models.EmailField()
    role       = models.CharField(max_length=20, choices=[
        ('hr',       'HR'),
        ('manager',  'Manager'),
        ('applicant','Applicant'),
        ('team_member', 'Team Member')
    ])
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_invites'
    )
    status     = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        
        return timezone.now() > self.expires_at
    
class Profile(models.Model):

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
    user       = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    location = models.CharField(max_length=100,blank=True,null=True)
    experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES)
    salary=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    job_type= models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    skills=models.JSONField(default=list)
   

    def __str__(self):
        return f"{self.user.email}'s profile"
 
 


 





   
