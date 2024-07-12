from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from Users.models import (
    AdminUser, BaseAuthModel
)

@receiver(post_save,sender=AdminUser)
def update_base_auth_model(sender,instance,created,**kwargs):
    password = make_password(instance.password)
    if created:
        base_auth_instance, created = BaseAuthModel.objects.update_or_create(
            username = instance.username,
            email = instance.email,
            defaults={
                'password':password,
            }
        )
    else:
        base_auth_instance = BaseAuthModel.objects.filter(username=instance.username).first()
        if base_auth_instance:
            base_auth_instance.email = instance.email
            base_auth_instance.password = make_password(instance.password)
            base_auth_instance.save()
            