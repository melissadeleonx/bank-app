# Signals.py to create UserProfile and Account instances whenever a new User is created.
# #TODO: UserProfile and Account are created after a user is registered. With restrictions like 2fa_completed boolean, the signals won't work. Needs fixing!

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile, Account

@receiver(post_save, sender=User)
def create_user_profile_and_account(sender, instance, created, **kwargs):
    if created:
        # A new User instance has been created. Create the associated UserProfile.
        UserProfile.objects.create(user=instance)
        
        Account.objects.create(
        user=instance,
        account_number=f'{instance.id:010d}',  
        account_type=Account.SAVINGS, 
        balance=0.00  
        )
