from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from annoying.fields import AutoOneToOneField


# Model constants
CONTENT_LENGTH = 140
USERNAME_LENGTH = 16
COLOR_DEFAULT = '#FFE0B2'
COLOR_MAX_LENGTH = 10

# Object Models

class Account(models.Model):
    """
    A collection of additional data about a User not stored
    directly on the Auth.User object.
    """
    # Links information to an Auth.User. Because this is
    # a OneToOne field, the creation of this field
    # automatically triggers the creation of the reference
    # from the user model to the account model.
    user = models.OneToOneField(
        'auth.User',
        primary_key=True,
        on_delete=models.CASCADE,
    )

    # This is a non-reflexive relationship, i.e.
    # just because you're my friend dosn't mean
    # I'm yours.
    friends = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True
    )

    # There's also technically some feed association
    # here, but the implementation of the many-to-one
    # field is handled in the Feed object.


    # String representation override
    def __unicode__(self):
        return '%s' % (self.user)


class Feed(models.Model):
    """
    A single content object that might otherwise be called
    a 'post'.
    """
    created = models.DateTimeField(auto_now_add=True)
    author  = models.ForeignKey('Account', related_name='posts')
    content = models.CharField(max_length=CONTENT_LENGTH)
    color   = models.CharField(default=COLOR_DEFAULT, max_length=COLOR_MAX_LENGTH)

    #recipients = models.ForeignKey('Account', related_name='inbox', null=True)
    recipients = models.ManyToManyField(
        'Account',
        related_name="inbox",
        blank=True,
        symmetrical=True,
    )


    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return '%s' % (self.content)
