from rest_framework import viewsets
from Pizzeria_Management.apps.accounts.serializers import ProfileSerializer
from Pizzeria_Management.apps.accounts.models import Profile


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
