from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


class RegisterUser(AbstractUser):
    phone_number = models.CharField(max_length=13, unique=True)
    access_token = models.CharField(max_length=255)

    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return self.phone_number


class UserPost(models.Model):
    owner = models.ForeignKey(RegisterUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.owner} title is {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(UserPost, self).save(*args, **kwargs)
