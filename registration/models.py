from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

def custom_upload_to(instance, filename):
    old_instance = Profile.objects.get(pk=instance.pk)
    old_instance.avatar.delete()
    return 'profiles_images/' + filename


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=custom_upload_to, null=True, blank=True, help_text="Enter a avatar image", verbose_name="Avatar") 
    bio = models.TextField(null=True, blank=True, help_text="Enter a bio", verbose_name="Bio")
    link = models.URLField(max_length=210, null=True, blank=True, help_text="Enter a personal website", verbose_name="Website")

    class Meta:
        verbose_name = "perfil"
        verbose_name_plural = "perfiles"
        ordering = ['user__username', ]
    """

    def get_absolute_url(self):
        return ""#reverse_lazy('category-detail', args=[str(self.id)])

    def soft_delete(self):
        self.active = False
        self.save()

    def __str__(self):
        return self.name
    """

@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    """
    Señal que se encarga de crear un perfil por defecto en caso de que 
    el usuario se cree una cuenta (post_save) pero nunca ingrese a su perfil.
    """
    if kwargs.get('created', False): # Si acaba de crearse un usuario creamos el perfil
        Profile.objects.get_or_create(user=instance)
        # print("Se acaba de crear un usuario y su perfil enlazado.")