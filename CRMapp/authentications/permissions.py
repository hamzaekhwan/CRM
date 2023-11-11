from CRMapp.models import *
from rest_framework import permissions

class IsAuthenticatedAndIsMaint(permissions.BasePermission):
  
    def has_permission(self, request, view):
        # تحقق مما إذا كان المستخدم مصادق عليه
        is_authenticated = bool(request.user and request.user.is_authenticated)

        # تحقق مما إذا كان لدى المستخدم isMaint = True في UserProfile
        try:
            is_maint = request.user.userprofile.isMaint
        except UserProfile.DoesNotExist:
            is_maint = False

        return is_authenticated and is_maint