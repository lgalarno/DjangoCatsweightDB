from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import datetime

import os

def upload_location(instance, filename):
    return "{0}/{1}".format(instance, filename)

class Cat(models.Model):
    name        = models.CharField(max_length=30, unique=True)
    slug        = models.SlugField(max_length=30)
    description = models.TextField(blank=True)
    birth       = models.IntegerField(null=True, blank=True)
    picture     = models.ImageField(upload_to = upload_location,
                              null=True,
                              blank=True)
    timestamp   = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated     = models.DateTimeField(auto_now_add=False, auto_now=True)
    active      = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('CatsManagement:CatDetailView', args=[self.id, self.slug])

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Cat, self).save(*args, **kwargs)

    @property
    def age(self):
        if self.birth:
            return datetime.now().year - self.birth
        else:
            return None


@receiver(models.signals.post_delete, sender=Cat)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Player` object is deleted.
    """
    if instance.picture:
        if os.path.isfile(instance.picture.path):
            os.remove(instance.picture.path)

@receiver(models.signals.pre_save, sender=Cat)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Player` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_picture = Cat.objects.get(pk=instance.pk).picture
    except Cat.DoesNotExist:
        return False

    new_picture = instance.picture
    if not old_picture == new_picture:
        if os.path.isfile(old_picture.path):
            os.remove(old_picture.path)