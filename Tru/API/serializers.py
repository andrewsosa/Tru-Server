from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

from API.models import Feed, Account


class AccountSerializer(serializers.ModelSerializer):
    feeds = serializers.StringRelatedField(
        many=True,
        #queryset=Feed.objects.all()
        read_only=True,
    )

    user = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='User-detail',
    )

    class Meta:
        model = Account
        fields = ('user', 'feeds')


class UserSerializer(serializers.ModelSerializer):
    account = serializers.HyperlinkedRelatedField(
        required=False,
        read_only=True,
        view_name='Account-detail',
    )

    email = serializers.EmailField(
        # This requires the email to be submitted
        # since the default dosn't require one.
        allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all())]

    )

    password = serializers.CharField(
        # This protects the password from ever being
        # returned over a request.
        write_only=True,
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'account')
        read_only_fields = ('account',)

    def create(self, validated_data):
        # Automatically populate all the data into their
        # matching fields.
        user = User.objects.create(**validated_data)

        # This step will use the provided .set_password
        # method to hash and store the user password.
        user.set_password(validated_data['password'])
        user.save()

        # In this step we create the corresponding
        # account profile for this user.
        Account.objects.create(user=user)
        return user


class FeedSerializer(serializers.ModelSerializer):
    author = serializers.HyperlinkedRelatedField(
        #queryset = Account.objects.filter(user=self.request.user.id)
        read_only = True,
        view_name = 'Account-detail',
    )

    class Meta:
        model = Feed
        fields = ('id', 'created', 'author', 'content', 'color')
