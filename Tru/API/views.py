from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse

from API.serializers import UserSerializer, FeedSerializer, AccountSerializer
from API.permissions import AccountPermission, FeedPermission, UserPermission
from API.models import Feed, Account

# Class-based views.

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for data on users.
    """
    serializer_class = UserSerializer
    permission_classes = [UserPermission]

    def get_queryset(self):
        #return User.objects.all()

        if self.request.user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.filter(id=self.request.user.id)

    @api_view(['POST'])
    def create_auth(request):
        serialized = UserSerializer(data=request.data)
        if serialized.is_valid():
            serialized.create(serialized.validated_data)
            return Response(serialized.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

class AccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint for user account data.
    """
    serializer_class = AccountSerializer
    permission_classes = [AccountPermission]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Account.objects.all()
        else:
            return Account.objects.filter(user=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FeedViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Feed content.
    """
    serializer_class = FeedSerializer
    permission_classes = [FeedPermission]

    def get_queryset(self):
        # Allow admins to view all of the posts.
        if self.request.user.is_staff:
            return Feed.objects.all()

        # Try and retrieve the account for the authenicated user.
        try:
            account = Account.objects.get(user=self.request.user.id)
            return Feed.objects.filter(author=account)
        except Account.DoesNotExist:
            return None

        # TODO:
        # If a non-staff user without a linked account attempts to
        # access the feeds, the above exception handler might not
        # catch it, as it could throw in the self.request.user.id
        # lookup. However, due to permission settings, it is
        # unlikely such a user would execute this code.


    def perform_create(self, serializer):
        #user = User.objects.get(id=self.request.user.id)
        account = Account.objects.get(user=self.request.user.id)
        serializer.save(author=account)
