from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import Customer


# TODO -> signals are not working  i have to remove the bugs in it
def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)

        Customer.objects.create(
            user=instance,
            name=instance.username
        )
        print('profile created.....!!!')


post_save(customer_profile, sender=User)



