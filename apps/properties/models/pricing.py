from django.db import models

class PricingRule(models.Model):
    """
    Dynamic pricing rules for seasonal or demand-based rent adjustments.
    Covers: USP 4 (Dynamic Pricing Engine)
    """
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='pricing_rules')
    rule_name = models.CharField(max_length=100, help_text="e.g., Summer Surge")
    start_month = models.IntegerField(choices=[(i, i) for i in range(1, 13)], help_text="1=January, 12=December", db_index=True)
    end_month = models.IntegerField(choices=[(i, i) for i in range(1, 13)], db_index=True)
    price_multiplier = models.DecimalField(max_digits=3, decimal_places=2, help_text="e.g., 1.10 for 10% increase")
    
    def __str__(self):
        return f"{self.rule_name} ({self.price_multiplier}x)"
