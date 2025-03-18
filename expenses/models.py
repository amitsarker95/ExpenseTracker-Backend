from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal

class Category(models.Model):

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='expenses', on_delete=models.CASCADE, null=True)
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='incomes', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.title} - {self.amount}"

class Budget(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='budgets',
        on_delete=models.CASCADE,
        null=True
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='Budget')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['category', 'user'],
                condition=models.Q(end_date__gte=models.F('start_date')),
                name='unique_active_budget_per_category'
            )
        ]

    def clean(self):
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError("Start date must be before end date")

            # Check for overlapping budgets
            overlapping_budget = Budget.objects.filter(
                category=self.category,
                user=self.user,
                start_date__lte=self.end_date,
                end_date__gte=self.start_date
            ).exclude(pk=self.pk).first()

            if overlapping_budget:
                raise ValidationError(
                    f"A budget for {self.category.name} already exists for this period "
                    f"(from {overlapping_budget.start_date} to {overlapping_budget.end_date})"
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.first_name if self.user else 'No User'} {self.category.name} - {self.amount}"

    @property
    def remaining_amount(self):
        total_expenses = Expense.objects.filter(
            category=self.category,
            date__range=[self.start_date, self.end_date]
        ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0')
        return self.amount - total_expenses

    @property
    def total_expenses(self):
        return Expense.objects.filter(
            category=self.category,
            date__range=[self.start_date, self.end_date]
        ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0')


class RecurringExpense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='recurring_expenses', on_delete=models.CASCADE, null=True)
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

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='transactions', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField()
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)

    def __str__(self):
        return f"{self.user.first_name} {self.title} - {self.amount} ({self.transaction_type})"
    

class SavingsGoal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='savings_goals', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    target_date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.title} - Target: {self.target_amount}, Current: {self.current_amount}"

