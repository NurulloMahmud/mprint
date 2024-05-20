from rest_framework import serializers
from .models import ExpenseCategory, Expenses



class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = '__all__'
    

class ExpensesReadSerializer(serializers.ModelSerializer):
    category = ExpenseCategory()

    class Meta:
        model = Expenses
        fields = '__all__'
    
    def create(self, validated_data):
        category = validated_data.pop('category')
        category_obj = ExpenseCategory.objects.get(id=category['id'])
        expense = Expenses.objects.create(category=category_obj, **validated_data)
        return expense
    def update(self, instance, validated_data):
        category = validated_data.pop('category')
        category_obj = ExpenseCategory.objects.get(id=category['id'])
        instance.category = category_obj
        return super().update(instance, validated_data)
    
