from rest_framework.permissions import BasePermission

from .models.advertisement import Advertisement
from .models.order import Order


class OrderTaker(BasePermission):

    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Object level permission, allow editing self"""
        return self.has_permission(request, view) and request.user == obj.taker


class OrderMaker(BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Object level permission, allow editing self"""
        return self.has_permission(request, view) and request.user == obj.maker


class IsOrderTaker(BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Object level permission, allow editing self"""
        return self.has_permission(request, view) and request.user == obj.taker


class IsOrderMaker(BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Object level permission, allow editing self"""
        return self.has_permission(request, view) and request.user == obj.maker


class OrderIsOpen(BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Object level permission, allow editing self"""
        return self.has_permission(request, view) and obj.status == Order.OPEN
