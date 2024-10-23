from django.contrib import admin
from .models import ChatModel

@admin.register(ChatModel)
class ChatModelAdmin(admin.ModelAdmin):
    list_display = ('user_message', 'answers', 'image_path', 'video_path')  # Fields to display in the list view
    search_fields = ('user_message', 'answers')  # Fields that can be searched in the admin
    list_filter = ('image_path', 'video_path')  # Optional: Filters for admin list view

    # Optional: Customizing the form layout in the admin
    # fieldsets = (
    #     (None, {
    #         'fields': ('user_message', 'answers')
    #     }),
    #     ('Media', {
    #         'fields': ('image_path', 'video_path')
    #     }),
    # )

