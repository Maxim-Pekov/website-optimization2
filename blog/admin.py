from django.contrib import admin
from blog.models import Post, Tag, Comment
from django.utils.safestring import mark_safe
from django.utils.html import format_html


@admin.register(Post)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('title', 'text', 'preview', 'slug', 'image', 'published_at', 'author', 'likes', 'tags',)
    list_display = ('title', 'image_tag', 'text', 'published_at',)
    list_display_links = ('title',)
    readonly_fields = ('slug', 'published_at', 'preview')
    raw_id_fields = ('author', 'likes', 'tags',)

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" style="max-height: 200px;">')


@admin.register(Tag)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', )


@admin.register(Comment)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('text', 'published_at', 'author', 'post',)
    list_display = ('text', 'published_at')
    list_display_links = ('text',)
    readonly_fields = ('published_at',)
    raw_id_fields = ('post', 'author',)



