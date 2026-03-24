from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import TeamInvite
from datetime import timezone,timedelta

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
  name = serializers.CharField(max_length=100, required=True, allow_blank=False) 
  password = serializers.CharField(max_length=68,min_length=8,write_only=True,required=True)
  confirm_password =serializers.CharField(max_length=68,min_length=8,write_only=True,required=True)
  role = serializers.CharField(max_length=100,required=True,allow_blank=False)
    

  class Meta:
   model = User
   fields=['name','email','password','confirm_password','role']
  
  def validate(self, attrs):
          if attrs['password'] != attrs['confirm_password']:
              raise serializers.ValidationError({"password": "Passwords do not match."})
          return attrs
    
  def create(self,validated_data):
   validated_data.pop('confirm_password') 
   return User.objects.create_user(**validated_data)
  


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=68,write_only=True,min_length=8)
    token = serializers.CharField(max_length=255,min_length=8,read_only=True)

    class Meta:
        model=User
        fields = ['email','password','token']  

class SendInviteSerializer(serializers.ModelSerializer):
   class Meta:
      model  = TeamInvite
      fields =['email','role'] 
    
   def validate_email(self,value):
        if TeamInvite.objects.filter(email = value,status='pending').exists():
           raise serializers.ValidationError("A pending invite already exists for this email.")
        
        if User.objects.filter(email=value).exists():
         raise serializers.ValidationError("A user with this email already exists.")
        return value
   

   def create(self, validated_data):
        return TeamInvite.objects.create(
            **validated_data,
            invited_by=self.context['request'].user,
            expires_at=timezone.now() + timedelta(days=7)
        )
   
class AcceptInviteSerializer(serializers.ModelSerializer):
    token     = serializers.UUIDField()
    username  = serializers.CharField()
    password  = serializers.CharField(write_only=True)

    def validate_token(self, value):
        try:
            invite = TeamInvite.objects.get(token=value, status='pending')
        except TeamInvite.DoesNotExist:
            raise serializers.ValidationError("Invalid or already used invite.")

        if invite.is_expired():
            invite.status = 'expired'
            invite.save()
            raise serializers.ValidationError("This invite has expired.")

        return value