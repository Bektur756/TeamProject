from rest_framework.permissions import BasePermission


class IsAuthorOrIsAdmin(BasePermission):
    # create, listing
    # def has_permission(self, request, view):

    # update, partial_update, destroy, retrieve
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user == obj.author, not request.user.is_owner


class IsOwnerOrIsAdmin(BasePermission):
    # create, listing
    # def has_permission(self, request, view):

    # update, partial_update, destroy, retrieve
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user.is_owner
