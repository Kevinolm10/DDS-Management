from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('contact_id', 'created_at')
    list_editable = ('is_read',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:  # If it's an existing contact, make contact_id read-only
            readonly_fields = readonly_fields + ('contact_id',)
        return readonly_fields
