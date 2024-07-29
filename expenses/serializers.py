from rest_framework import serializers
from .models import Category, Expense, Income, Budget

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ExpenseSerializer(serializers.ModelSerializer):
    
    user_name = serializers.ReadOnlyField(source="user_full_name")
    category_name = serializers.ReadOnlyField(source="category.name")
    category_choices = serializers.SerializerMethodField()

    class Meta:
        model = Expense
        fields = ['id','user_name','title','description','amount','category_name','category_choices','date']

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
    class Meta:
        model = Budget
        fields =['id','category','amount','start_date','end_date']

