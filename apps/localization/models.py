from django.db import models
import uuid

class TranslationString(models.Model):
    """
    Stores translations for app UI strings in multiple languages.
    Covers: Technical Feature 6 (Localization / Language Support)
    """
    class Languages(models.TextChoices):
        ENGLISH = 'en', 'English'
        HINDI = 'hi', 'Hindi'
        TAMIL = 'ta', 'Tamil'
        TELUGU = 'te', 'Telugu'
        KANNADA = 'kn', 'Kannada'
        BENGALI = 'bn', 'Bengali'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    module = models.CharField(max_length=50, help_text="App module name: e.g., 'mess', 'payroll', 'finance'", db_index=True)
    key = models.CharField(max_length=100, help_text="Translation key: e.g., 'mark_attendance', 'book_meal'")
    language = models.CharField(max_length=5, choices=Languages.choices, db_index=True)
    value = models.TextField(help_text="Translated text in the target language")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'SUPERADMIN'})
    
    class Meta:
        unique_together = ('module', 'key', 'language')
        indexes = [
            models.Index(fields=['module', 'language']),
            models.Index(fields=['key', 'language'])
        ]
    
    def __str__(self):
        return f"{self.module}.{self.key} ({self.language})"
