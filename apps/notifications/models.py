from django.db import models
import uuid

class NotificationLog(models.Model):
    """
    Logs all notifications sent to users.
    Covers: Technical Feature 1 (Notification System)
    """
    class NotificationType(models.TextChoices):
        SMS = 'SMS', 'SMS'
        EMAIL = 'EMAIL', 'Email'
        PUSH = 'PUSH', 'Push Notification'
        WHATSAPP = 'WHATSAPP', 'WhatsApp'

    class NotificationCategory(models.TextChoices):
        RENT_REMINDER = 'RENT_REMINDER', 'Rent Reminder'
        PAYMENT_SUCCESS = 'PAYMENT_SUCCESS', 'Payment Success'
        COMPLAINT_UPDATE = 'COMPLAINT_UPDATE', 'Complaint Update'
        NIGHT_ALERT = 'NIGHT_ALERT', 'Night Entry Alert'
        SOS_ALERT = 'SOS_ALERT', 'SOS Alert'
        NOTICE = 'NOTICE', 'Notice Board'
        GENERAL = 'GENERAL', 'General'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NotificationType.choices, db_index=True)
    category = models.CharField(max_length=30, choices=NotificationCategory.choices, db_index=True)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_sent = models.BooleanField(default=False, db_index=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.get_notification_type_display()} to {self.user.username}"

class FCMToken(models.Model):
    """
    Stores Firebase Cloud Messaging tokens for push notifications.
    Covers: Technical Feature 1 (Notification System)
    """
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='fcm_tokens')
    token = models.CharField(max_length=255, unique=True)
    device_type = models.CharField(max_length=20, choices=[('ANDROID', 'Android'), ('IOS', 'iOS'), ('WEB', 'Web')])
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"FCM Token for {self.user.username}"
