# permissions.py
from rest_framework.permissions import BasePermission

class IsHR(BasePermission):
    """Allow access only to HR users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'hr'

class IsManager(BasePermission):
    """Allow access only to Managers."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'manager'
    
class IsTeamMember(BasePermission):
    """Allow access only to Managers."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'team_member'
    
class IsHROrManager(BasePermission):
    """Allow access to HR or Manager users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['hr', 'manager']
    
class IsHROrManagerOrTeam(BasePermission):
    """Allow access to HR or Manager users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['hr', 'manager','team_member']

class IsApplicant(BasePermission):
    """Allow access only to Applicants."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'applicant'

class IsOwnerOrHR(BasePermission):
    """Applicants can only access their own data; HR can access all."""
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'hr':
            return True
        return obj.applicant == request.user  # ownership check