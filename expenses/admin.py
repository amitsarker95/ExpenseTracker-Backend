from django.contrib import admin
from .models import Category, Expense, Income, Budget, RecurringExpense, Transaction, SavingsGoal

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'amount', 'category', 'date')
    list_filter = ('category', 'date', 'user')
    search_fields = ('title', 'description', 'user__email')
    date_hierarchy = 'date'

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'amount', 'date')
    list_filter = ('date', 'user')
    search_fields = ('title', 'description', 'user__email')
    date_hierarchy = 'date'

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('category', 'user', 'amount', 'start_date', 'end_date')
    list_filter = ('category', 'user', 'start_date', 'end_date')
    search_fields = ('category__name', 'user__email')
    date_hierarchy = 'start_date'

@admin.register(RecurringExpense)
class RecurringExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'amount', 'category', 'recurrence_interval', 'start_date')
    list_filter = ('category', 'recurrence_interval', 'user')
    search_fields = ('title', 'description', 'user__email')
    date_hierarchy = 'start_date'

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'amount', 'category', 'transaction_type', 'date')
    list_filter = ('category', 'transaction_type', 'date', 'user')
    search_fields = ('title', 'description', 'user__email')
    date_hierarchy = 'date'

@admin.register(SavingsGoal)
class SavingsGoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'target_amount', 'current_amount', 'target_date')
    list_filter = ('user', 'target_date')
    search_fields = ('title', 'description', 'user__email')
    date_hierarchy = 'target_date'
