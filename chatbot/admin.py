from django.contrib import admin
from .models import ChatSession, ChatMessage, BusinessKnowledge

@admin.register(BusinessKnowledge)
class BusinessKnowledgeAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    search_fields = ['title', 'content']

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'user_name', 'step', 'created_at']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'is_user', 'message', 'created_at']
    list_filter = ['is_user']
