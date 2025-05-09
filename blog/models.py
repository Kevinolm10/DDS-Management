import cloudinary
import uuid
from django.db import models
from django_summernote.fields import SummernoteTextField


class Post(models.Model):
    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique UUID field
    image = cloudinary.models.CloudinaryField('image')
    title = models.CharField(max_length=200)
    content = SummernoteTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
