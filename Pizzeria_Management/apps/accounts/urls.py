from django.conf.urls import url, include
from rest_framework import routers

from Pizzeria_Management.apps.accounts.api.viewsets import ProfileViewSet

router = routers.DefaultRouter()
router.register(r'profile', ProfileViewSet)

urlpatterns =  [
    url(r'^', include(router.urls))
]