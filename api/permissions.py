from rest_framework.permissions import BasePermission

class IsownerORStaff(BasePermission):
	message = "You must be a owner or a staff."

	def has_object_permission(self, request, view, obj):
		if (obj.owner == request.user) or request.user.is_staff:
			return True
		else:
			return False

