from django.db import models
import uuid

class MessMenu(models.Model):
    """
    Weekly or daily menu for the mess.
    Covers: Module 6 (Smart Mess)
    """
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE)
    date = models.DateField(db_index=True)
    breakfast = models.CharField(max_length=255, null=True, blank=True)
    lunch = models.CharField(max_length=255, null=True, blank=True)
    dinner = models.CharField(max_length=255, null=True, blank=True)
    
    price_breakfast = models.DecimalField(max_digits=6, decimal_places=2)
    price_lunch = models.DecimalField(max_digits=6, decimal_places=2)
    price_dinner = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('property', 'date')

    def __str__(self):
        return f"Menu for {self.date} at {self.property.name}"
