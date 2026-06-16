import cloudinary
import uuid
from django.db import models
from django.utils.text import slugify
from django.core.validators import EmailValidator
from django_summernote.fields import SummernoteTextField

class agents(models.Model):
    agent_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = cloudinary.models.CloudinaryField('image')
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(validators=[EmailValidator()])
    phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        try:
            return self.image.url
        except Exception:
            return ""

class Contact(models.Model):
    contact_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator()])
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Players(models.Model):
    player_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = cloudinary.models.CloudinaryField('image')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    club = models.CharField(max_length=100, blank=True, null=True)
    description = SummernoteTextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        try:
            return self.image.url
        except Exception:
            return ""