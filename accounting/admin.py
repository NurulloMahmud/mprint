from django.contrib import admin
from .models import Expenses, ExpenseCategory, InventoryExpense, PaperExpenses


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'category', 'branch', 'date')



admin.site.register(Expenses, ExpenseAdmin)
admin.site.register(ExpenseCategory)
admin.site.register(InventoryExpense)
admin.site.register(PaperExpenses)