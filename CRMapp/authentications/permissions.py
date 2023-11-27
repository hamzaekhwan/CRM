from CRMapp.models import *
from rest_framework import permissions


class IsEmp(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            # تحقق مما إذا كان المستخدم مصادق عليه
            is_authenticated = bool(request.user and request.user.is_authenticated)

            # تحقق مما إذا كان لدى المستخدم isEmp = True في UserProfile
            try:
                isEmp = request.user.userprofile.isEmp
            except UserProfile.DoesNotExist:
                isEmp = False

            return is_authenticated and isEmp
        except:
            return False

class IsMaint(permissions.BasePermission):
  
    def has_permission(self, request, view):
        try:
            # تحقق مما إذا كان المستخدم مصادق عليه
            is_authenticated = bool(request.user and request.user.is_authenticated)

            # تحقق مما إذا كان لدى المستخدم isMaint = True في UserProfile
            try:
                is_maint = request.user.userprofile.isMaint
            except UserProfile.DoesNotExist:
                is_maint = False

            return is_authenticated and is_maint
        except:
            return False


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
    
            is_superuser = bool(request.user and request.user.is_superuser)

          
            try:
                
                isManager = request.user.userprofile.isManager
            except UserProfile.DoesNotExist:
                isManager = False
            
        
            return is_superuser and isManager
        except:
            return False

class IsManagerMaint(permissions.BasePermission):
  
    def has_permission(self, request, view):
        try:
            # تحقق مما إذا كان المستخدم مصادق عليه
            is_superuser = bool(request.user and request.user.is_superuser)

            # تحقق مما إذا كان لدى المستخدم isMaint = True في UserProfile
            try:
                isMangerMaint = request.user.userprofile.isMangerMaint
            except UserProfile.DoesNotExist:
                isMangerMaint = False

            return is_superuser and isMangerMaint    
        except:
            return False
    


class ApiKeyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # المفتاح الثابت
        static_api_key = "KIiCCxOfPUsM52BRdf7zJFeXKtfsT43iW2oU2L78MyhKJISRlidZcF8rw6LMyGzi"

        # استخراج مفتاح الرمز المميز من رأس الطلبات
        api_key = request.META.get('HTTP_AUTHORIZATION')

        if api_key:
            # تقطيع "Token " للحصول على القيمة الفعلية للمفتاح
            api_key = api_key.split(' ')[-1]

            # المقارنة مع المفتاح الثابت
            if api_key == static_api_key:
                return True

        # إذا كان المفتاح غير صحيح أو لم يتم إرساله
        return False
