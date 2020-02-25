from rest_framework import serializers

from Pizzeria_Management.apps.accounts.models import Profile


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['city', 'zip_code', 'street', 'house_number', 'flat_number', 'address_type']


class ProfileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Profile

        fields = ['first_name', 'phone_number']
