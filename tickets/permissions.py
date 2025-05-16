from rest_framework.permissions import BasePermission

#Check if authenticated as admin
class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

#Check if authenticated as agent
class IsAgentUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_agent