from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError

from rest_framework import status
from rest_framework.generics import DestroyAPIView, ListCreateAPIView, UpdateAPIView
from rest_framework.response import Response

from project.api import exceptions as exc
from project.api import serializers as sers
from project.api import permissions as perms
from project.api.models import Resource, User


def get_user(request, user_id):
    return request.user if user_id is None else User.objects.get(id=user_id)


class UserListView(ListCreateAPIView):
    permission_classes = [perms.IsAuthenticated, perms.AdminAccessPermission]

    def list(self, request):
        users = User.objects.all()
        serialized_users = sers.UserSerializer(users, many=True)
        return Response(serialized_users.data, status=status.HTTP_200_OK)

    def create(self, request):
        serialized_user = sers.UserSerializer(data=request.data)
        serialized_user.is_valid(raise_exception=True)
        user = serialized_user.create()
        serialized_user = sers.UserSerializer(user)
        return Response(serialized_user.data, status=status.HTTP_201_CREATED)


class UserDestroyView(DestroyAPIView):
    permission_classes = [perms.IsAuthenticated, perms.AdminAccessPermission]

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            raise exc.UserNotFoundFailed()

        serialized_user = sers.UserSerializer(user)
        user.delete()

        return Response(serialized_user.data, status=status.HTTP_200_OK)


class ResourceListView(ListCreateAPIView):
    permission_classes = [
        perms.IsAuthenticated,
        perms.CurrentUserPermission | perms.AdminAccessPermission,
    ]

    def list(self, request, user_id=None):
        user = get_user(request=request, user_id=user_id)
        resources = Resource.objects.filter(user__id=user.id).all()
        serialized_resources = sers.ResourceSerializer(resources, many=True)
        return Response(serialized_resources.data, status=status.HTTP_200_OK)

    def create(self, request, user_id=None):
        user = get_user(request=request, user_id=user_id)

        if (user.quota is not None) and (user.resource_set.count() == user.quota):
            raise exc.ResourceQuotaFailed()

        serialized_resource = sers.ResourceSerializer(data=request.data)
        serialized_resource.is_valid(raise_exception=True)

        try:
            resource = serialized_resource.create(user_id=user.id)
        except IntegrityError:
            raise exc.ResourceDuplicateFailed()

        serialized_resource = sers.ResourceSerializer(resource)
        return Response(serialized_resource.data, status=status.HTTP_201_CREATED)


class ResourceDestroyView(DestroyAPIView):
    permission_classes = [
        perms.IsAuthenticated,
        perms.CurrentUserPermission | perms.AdminAccessPermission,
    ]

    def delete(self, request, resource_id, user_id=None):
        user = get_user(request=request, user_id=user_id)

        try:
            resource = Resource.objects.get(id=resource_id, user__id=user.id)
        except ObjectDoesNotExist:
            raise exc.ResourceNotFoundFailed()

        serialized_resource = sers.ResourceSerializer(resource)
        resource.delete()
        return Response(serialized_resource.data, status=status.HTTP_200_OK)


class QuotaUpdateView(UpdateAPIView):
    permission_classes = [perms.IsAuthenticated, perms.AdminAccessPermission]

    def patch(self, request, user_id):
        serialized_user = sers.UserSerializer(data=request.data, partial=True)
        serialized_user.is_valid(raise_exception=True)
        new_quota = serialized_user.validated_data["quota"]

        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            raise exc.UserNotFoundFailed()

        if (new_quota is not None) and (user.resource_set.count() > new_quota):
            raise exc.ResourceMoreNewQuotaFailed()

        user.quota = new_quota
        user.save()
        serialized_user = sers.UserSerializer(user)
        return Response(serialized_user.data, status=status.HTTP_200_OK)
