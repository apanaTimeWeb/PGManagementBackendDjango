from django.db import models

class ChatLog(models.Model):
    """
    Logs interactions between students and the AI Chatbot.
    Covers: USP 14 (AI Chatbot)
    """
    tenant = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, limit_choices_to={'role': 'TENANT'})
    message = models.TextField(help_text="User's question")
    bot_response = models.TextField(help_text="AI's answer")
    intent = models.CharField(max_length=50, null=True, blank=True, help_text="Detected intent e.g., 'rent_query'", db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Chat by {self.tenant.username} at {self.timestamp}"
