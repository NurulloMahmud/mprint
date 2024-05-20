from django.db import models



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
    note = models.TextField()

    def __str__(self):
        return self.note

