from rest_framework import serializers

from project.api.models import Resource, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "quota", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
            "id": {"read_only": True},
        }

    def create(self):
        return User.objects.create_user(
            email=self.validated_data["email"],
            password=self.validated_data["password"],
        )


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ["id", "name"]
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def create(self, user_id):
        resource = Resource.objects.create(
            user_id=user_id,
            name=self.validated_data["name"],
        )
        resource.save()
        return resource
