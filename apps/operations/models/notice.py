from django.db import models

class Notice(models.Model):
    """
    Digital notice board for broadcasting messages.
    Covers: Advanced Feature 7 (Digital Notice Board)
    """
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_published = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return self.title
