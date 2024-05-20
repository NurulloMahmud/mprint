from django.contrib import admin
from .models import Expenses, ExpenseCategory


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'category', 'branch', 'date')



admin.site.register(Expenses, ExpenseAdmin)
admin.site.register(ExpenseCategory)