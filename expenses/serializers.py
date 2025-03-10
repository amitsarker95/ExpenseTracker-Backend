from rest_framework import serializers
from .models import Category, Expense, Income, Budget, RecurringExpense, SavingsGoal

class CategorySerializer(serializers.ModelSerializer):
    CATEGORY_CHOICES = ['RENT','FOOD', 'TRANSPORT', 'ENTERTAINMENT', 'HEALTH', 'UTILITIES', 'OTHER']
    class Meta:
        model = Category
        fields = ['id', 'name']

    def validate_name(self, value):
        if value not in self.CATEGORY_CHOICES:
            raise serializers.ValidationError("Invalid category name")
        return value


class ExpenseSerializer(serializers.ModelSerializer):
    # category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all()) 
    category_name = serializers.ReadOnlyField(source="category.name")
    # category_choices = serializers.SerializerMethodField()

    class Meta:
        model = Expense
        fields = ['id','title','description','amount','category','category_name','date']
        extra_kwargs = {
            'category': {'write_only': True}
        }

    def get_category_choices(self, obj):
        categories = Category.objects.all()
        return CategorySerializer(categories, many=True).data


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id','title', 'amount', 'date','description']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # representation['user'] = instance.user.first_name
        return representation
    

class BudgetSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source="category.name")
    class Meta:
        model = Budget
        fields =['id','category','amount','start_date','end_date', 'category_name']

    def get_category_choices(self, obj):
        categories = Category.objects.all()
        return CategorySerializer(categories, many=True).data
    

class RecurringExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringExpense
        fields = ['title', 'description', 'amount', 'category', 'start_date', 'recurrence_interval']

class SavingsGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsGoal
        fields = ['title', 'target_amount','current_amount', 'target_date', 'description']

    

