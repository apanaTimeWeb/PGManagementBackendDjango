from django.db import models
from .menu import MessMenu

class DailyMealSelection(models.Model):
    """
    Tenant's daily choice for meals, enabling the pay-per-day wallet system.
    Covers: USP 15 (Pay-per-Day Mess Wallet)
    """
    class MealStatus(models.TextChoices):
        EATING = 'EATING', 'Eating'
        SKIPPING = 'SKIPPING', 'Skipping'

    tenant = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, limit_choices_to={'role': 'TENANT'})
    menu = models.ForeignKey(MessMenu, on_delete=models.CASCADE)
    
    breakfast_status = models.CharField(max_length=10, choices=MealStatus.choices, default=MealStatus.EATING, db_index=True)
    lunch_status = models.CharField(max_length=10, choices=MealStatus.choices, default=MealStatus.EATING, db_index=True)
    dinner_status = models.CharField(max_length=10, choices=MealStatus.choices, default=MealStatus.EATING, db_index=True)
    
    is_billed = models.BooleanField(default=False, help_text="True once the cost is debited from wallet.", db_index=True)

    class Meta:
        unique_together = ('tenant', 'menu')

    def __str__(self):
        return f"Meal selection for {self.tenant.username} on {self.menu.date}"
