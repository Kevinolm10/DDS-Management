from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at',)

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'is_published', 'created_at', 'updated_at')
    list_filter = ('category', 'is_featured', 'is_published', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_editable = ('is_featured', 'is_published')

    summernote_fields = ('content',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'image')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_published')
        }),
        ('Metadata', {
            'fields': ('post_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    readonly_fields = ('post_id', 'created_at', 'updated_at')
