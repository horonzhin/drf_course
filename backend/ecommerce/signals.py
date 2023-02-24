from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User, weak=False)
# receiver - receiver for the specified signal
# post_save - after something has been saved, we get a signal
# sender - table where saving (creating a user) takes place that sends a signal
def report_uploaded(sender, instance, created, **kwargs):
    """Every time a new user is created, a token is assigned to him, we do this using a signal"""
    if created:
        Token.objects.create(user=instance)
