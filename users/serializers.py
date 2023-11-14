from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ["user"]


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    current_user = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "current_user", "profile"]
        extra_kwargs = {"password": {"write_only": True, "required": False}}

    def create(self, validated_data):
        profile_data = validated_data.pop("profile")
        current_user = validated_data.pop("current_user", None)
        user_type = profile_data.get("type")
        validated_data["password"] = make_password(validated_data["password"])
        user = super().create(validated_data)
        profile_data["reference_id"] = current_user
        UserProfile.objects.create(user=user, **profile_data)

        if user_type == "doctor":
            update_user = UserProfile.objects.get(user__id=current_user)
            update_user.reference = user
            update_user.save()

        return user

    def update(self, instance, validated_data):
        if "password" in validated_data:
            instance.password = make_password(validated_data["password"])
            validated_data.pop("password")
        profile_data = validated_data.pop("profile", None)
        user = super().update(instance, validated_data)
        if profile_data:
            profile = user.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        return user
