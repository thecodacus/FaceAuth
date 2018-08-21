from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class FaceSignature(models.Model):
	user=models.OneToOneField(User, on_delete=models.CASCADE)
	signatures=models.TextField(null=True)
	face=models.TextField(null=True)
	def __str__(self):
		return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        FaceSigneture.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.facesigneture.save()


