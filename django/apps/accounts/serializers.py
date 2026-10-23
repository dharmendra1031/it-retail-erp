from rest_framework import serializers

from .models import Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("id", "name")
        read_only_fields = ("id",)

    def validate_name(self, name):
        name = name.strip()
        if not name:
            raise serializers.ValidationError("Role name is required.")

        roles = Role.objects.filter(name__iexact=name)
        if self.instance:
            roles = roles.exclude(pk=self.instance.pk)
        if roles.exists():
            raise serializers.ValidationError("Role name already exists.")

        return name
