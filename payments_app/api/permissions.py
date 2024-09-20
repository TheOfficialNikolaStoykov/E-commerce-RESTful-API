from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Check if the user is an admin
        if request.user and request.user.is_staff:
            print("User is admin:", request.user.username)  # Debug line
            return True

        # Check if the user is the owner of the order
        is_owner = obj.order.user == request.user
        print("Is owner:", is_owner)  # Debug line
        return is_owner