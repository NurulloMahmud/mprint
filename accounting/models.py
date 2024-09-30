from typing import Iterable
from django.db import models
from main.models import Inventory, Order, Paper


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Expenses(models.Model):
    date = models.DateField(auto_now_add=True)
    name = models.TextField()
    amount = models.DecimalField(decimal_places=2, max_digits=40)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    branch = models.ForeignKey('main.Branch', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date']

class Debt(models.Model):
    created_at = models.DateField(auto_now_add=True)
    amount = models.DecimalField(decimal_places=2, max_digits=40)
    date = models.DateField(null=True, blank=True)
    note = models.TextField()

    def __str__(self):
        return self.note

class InventoryExpense(models.Model):
    item = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="inventory_expenses")
    quantity = models.FloatField()
    amount = models.DecimalField(decimal_places=2, max_digits=40, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    branch = models.ForeignKey('main.Branch', on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.amount = self.item.cost * int(self.quantity or 0)
        self.branch = self.item.branch
        self.item.available -= self.quantity
        self.item.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.item.name

class PaperExpenses(models.Model):
    created_at = models.DateField(auto_now_add=True)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="paper_expenses")
    quantity = models.IntegerField()
    amount = models.DecimalField(decimal_places=2, max_digits=40, null=True, blank=True)
    branch = models.ForeignKey('main.Branch', on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.amount = self.paper.price * self.quantity
        self.branch = self.paper.branch
        super().save(*args, **kwargs)

