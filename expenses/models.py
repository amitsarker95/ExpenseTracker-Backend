from django.conf import settings
from django.db import models

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('FOOD', 'Food'),
        ('TRANSPORT', 'Transport'),
        ('ENTERTAINMENT', 'Entertainment'),
        ('HEALTH', 'Health'),
        ('UTILITIES', 'Utilities'),
        ('OTHER', 'Other'),
    ]

    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()

class Expense(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='exenses', on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.user.first_name} {self.title} - {self.amount}"
