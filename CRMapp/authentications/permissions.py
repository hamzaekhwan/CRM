from CRMapp.models import *
from rest_framework import permissions


class IsEmp(permissions.BasePermission):
    def has_permission(self, request, view):
        # تحقق مما إذا كان المستخدم مصادق عليه
        is_authenticated = bool(request.user and request.user.is_authenticated)

        # تحقق مما إذا كان لدى المستخدم isMaint = True في UserProfile
        try:
            isEmp = request.user.userprofile.isEmp
        except UserProfile.DoesNotExist:
            isEmp = False

        return is_authenticated and isEmp

class IsMaint(permissions.BasePermission):
  
    def has_permission(self, request, view):
        # تحقق مما إذا كان المستخدم مصادق عليه
        is_authenticated = bool(request.user and request.user.is_authenticated)

        # تحقق مما إذا كان لدى المستخدم isMaint = True في UserProfile
        try:
            is_maint = request.user.userprofile.isMaint
        except UserProfile.DoesNotExist:
            is_maint = False

        return is_authenticated and is_maint


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        # تحقق مما إذا كان المستخدم مصادق عليه
        is_superuser = bool(request.user and request.user.is_superuser)

        # تحقق مما إذا كان لدى المستخدم isMaint = True في UserProfile
        try:
            
            isManager = request.user.userprofile.isManager
        except UserProfile.DoesNotExist:
            isManager = False
        
      
        return is_superuser and isManager

class IsManagerMaint(permissions.BasePermission):
  
    def has_permission(self, request, view):
        # تحقق مما إذا كان المستخدم مصادق عليه
        is_superuser = bool(request.user and request.user.is_superuser)

        # تحقق مما إذا كان لدى المستخدم isMaint = True في UserProfile
        try:
            isMangerMaint = request.user.userprofile.isMangerMaint
        except UserProfile.DoesNotExist:
            isMangerMaint = False

        return is_superuser and isMangerMaint    