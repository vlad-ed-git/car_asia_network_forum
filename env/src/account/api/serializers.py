from rest_framework import serializers
from account.models import Account


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['email',  'display_name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self):

        account = Account(
            email=self.validated_data['email'],
            display_name=self.validated_data['display_name']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Passwords must match.'})
        account.set_password(password)
        account.save()
        return account


class AccountPropertiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['pk', 'email',  'display_name']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)
