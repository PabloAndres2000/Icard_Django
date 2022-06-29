# Django Rest Framework
from attr import field
from rest_framework import serializers

# Models (User)
from icard.apps.users.models import User

# Providers (User)
from icard.apps.users.providers import user as user_providers
from icard.utils.constants import TRY_AGAIN_LATER

# Utils (Error_handler)
from icard.utils.error_handler import ErrorHandler


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "identification_number",
            "email",
            "phone_number",
            "ip_address",
            "is_staff",
            "created_at",
            "updated_at",
            "is_active",
        ]


class UserSignUpSerializer(serializers.Serializer):
    """
    User sign up serializer.
    """
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    identification_number = serializers.CharField(max_length=20)
    email = serializers.EmailField(max_length=255)
    phone_number = serializers.CharField(max_length=15)
    password = serializers.CharField(min_length=5)

    def validate(self, data):

        error_handler = ErrorHandler()
        if user_providers.get_user_by_email(email=data["email"].lower()):
            error_handler.handler_error(
                field_name="email",
                error=TRY_AGAIN_LATER,
            )
        if user_providers.get_user_by_identification_number(identification_number=data["identification_number"].lower()
                                                            ):
            error_handler.handler_error(
                field_name="identification_number",
                error=TRY_AGAIN_LATER
            )
        if error_handler.have_errors():
            raise error_handler.raise_errors()
        return data

    def create(self, validated_data):
        user = user_providers.create_user(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            identification_number=validated_data["identification_number"],
            phone_number=validated_data["phone_number"],
            email=validated_data["email"],
            ip_address=self.context.get("ip_address"),
            password=validated_data["password"],
        )
        return user


class UpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    identification_number = serializers.CharField(max_length=20)
    email = serializers.EmailField(max_length=255)
    phone_number = serializers.CharField(max_length=15)

    def validate(self, data):
        instance = getattr(self, "instance", None)
        same_email = instance.email == data["email"]
        same_identification_number = (
            instance.identification_number == data["identification_number"]
        )

        error_handler = ErrorHandler()

        if (
            user_providers.get_user_by_email(email=data["email"].lower())
            and not same_email
        ):
            error_handler.handle_error(
                field_name="email",
                error="Ya existe un usuario con este email",
            )
        if (
            user_providers.get_user_by_identification_number(
                identification_number=data["identification_number"].lower()
            )
            and not same_identification_number
        ):
            error_handler.handle_error(
                field_name="identification_number",
                error="Ya existe un usuario con este rut",
            )
        if error_handler.have_errors():
            raise error_handler.raise_errors()
        return data

    def update(self, instance, validated_data):
        user = user_providers.update_user_by_pk(
            user_pk=int(instance.pk), **validated_data)
        return user


class UpdatePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=255)

    class Meta:
        model = User
        fields = [
            "id",
            "password",
        ]

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save(update_field=["password", "updated_at"])
        return instance
