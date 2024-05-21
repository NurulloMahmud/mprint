from rest_framework import serializers
from .models import ExpenseCategory, Expenses
from main.serializers import BranchSerializer
from main.models import Branch, PaymentMethod



class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = '__all__'
    

class ExpensesReadSerializer(serializers.ModelSerializer):
    category = ExpenseCategory()
    branch = BranchSerializer()

    class Meta:
        model = Expenses
        fields = '__all__'
    
    def create(self, validated_data):
        branch = validated_data.pop('branch')
        branch_obj = Branch.objects.get(id=branch['id'])
        category = validated_data.pop('category')
        category_obj = ExpenseCategory.objects.get(id=category['id'])
        expense = Expenses.objects.create(category=category_obj, branch=branch_obj, **validated_data)
        return expense
    
    def update(self, instance, validated_data):
        branch = validated_data.pop('branch')
        branch_obj = Branch.objects.get(id=branch['id'])
        category = validated_data.pop('category')
        category_obj = ExpenseCategory.objects.get(id=category['id'])
        instance.category = category_obj
        instance.branch = branch_obj
        return super().update(instance, validated_data)
    

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

