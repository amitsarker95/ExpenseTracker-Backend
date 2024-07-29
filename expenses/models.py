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
        return self.name

class Expense(models.Model):

    # user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='exenses', on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.user.first_name} {self.title} - {self.amount}"
    
    @property
    def user_full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    

class Income(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='incomes', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.title} - {self.amount}"

class Budget(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='budgets', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.user.first_name} {self.category.name} - {self.amount}"


class RecurringExpense(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='recurring_expenses', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    start_date = models.DateField()
    recurrence_interval = models.CharField(max_length=50, choices=[
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('YEARLY', 'Yearly')
    ])

    def __str__(self):
        return f"{self.user.first_name} {self.title} - {self.amount} ({self.recurrence_interval})"
    
    
class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('EXPENSE', 'Expense'),
        ('INCOME', 'Income'),
    ]

    # user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='transactions', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField()
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)

    def __str__(self):
        return f"{self.user.first_name} {self.title} - {self.amount} ({self.transaction_type})"
    

class SavingsGoal(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='savings_goals', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    target_date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.title} - Target: {self.target_amount}, Current: {self.current_amount}"

