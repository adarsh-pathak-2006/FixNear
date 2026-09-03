from rest_framework.permissions import BasePermission

class IsTechnician(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role=='TECHNICIAN'

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role=='CUSTOMER'

class IsTechnicianAndCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['CUSTOMER', 'TECHNICIAN']