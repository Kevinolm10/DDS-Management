from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post

# Register the Post model in the admin interface with customized settings
@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):  # Extend SummernoteModelAdmin to enable Summernote integration
    list_display = ('image', 'title', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'  # Allows filtering by date
    ordering = ('-created_at',)  # Orders posts by created_at in descending order

    summernote_fields = ('content',)  # Add Summernote editor for 'content' field

    # Optional: If you want to use post_id in the admin interface
    def get_readonly_fields(self, request, obj=None):
        """Make post_id read-only in admin"""
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:  # If it's an existing post, make post_id read-only
            readonly_fields = readonly_fields + ('post_id',)
        return readonly_fields
