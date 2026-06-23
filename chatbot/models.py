from django.db import models
from services.models import Service


class ChatSession(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    user_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    service = models.ForeignKey(Service, null=True, blank=True, on_delete=models.SET_NULL)
    selected_date = models.DateField(null=True, blank=True)
    selected_time = models.CharField(max_length=10, blank=True)
    step = models.CharField(max_length=50, default='greeting')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def reset(self):
        self.user_name = ''
        self.phone = ''
        self.service = None
        self.selected_date = None
        self.selected_time = ''
        self.step = 'greeting'
        self.save()

    def __str__(self):
        return f"Session {self.session_id} - {self.user_name or 'Guest'}"


class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    is_user = models.BooleanField(default=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        role = 'User' if self.is_user else 'Bot'
        return f"{role}: {self.message[:50]}"


class BusinessKnowledge(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Business Knowledge'
        verbose_name_plural = 'Business Knowledge'
