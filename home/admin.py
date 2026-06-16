from django.contrib import admin
from .models import Contact, Players, agents

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
        if obj:
            readonly_fields = readonly_fields + ('contact_id',)
        return readonly_fields


@admin.register(Players)
class PlayersAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'club', 'created_at')
    search_fields = ('name', 'position', 'club', 'description')
    readonly_fields = ('player_id', 'created_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:
            readonly_fields = readonly_fields + ('player_id',)
        return readonly_fields


@admin.register(agents)
class AgentsAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'email', 'phone', 'created_at')
    search_fields = ('name', 'position', 'email')
    readonly_fields = ('agent_id', 'created_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:
            readonly_fields = readonly_fields + ('agent_id',)
        return readonly_fields