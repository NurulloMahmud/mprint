from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError



class Stakeholder(models.Model):
    name = models.CharField(max_length=100)
    percent = models.IntegerField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            total = Stakeholder.objects.aggregate(Sum('percent'))['percent__sum'] or 0
            if total + self.percent > 100:
                raise ValidationError("Umumiy fonding balansi 100% dan oshmasligi kerak")
        else:
            total = Stakeholder.objects.exclude(pk=self.pk).aggregate(Sum('percent'))['percent__sum'] or 0
            if total + self.percent > 100:
                raise ValidationError("Umumiy fonding balansi 100% dan oshmasligi kerak")
            
        super().save(*args, **kwargs)


class BalanceSheet(models.Model):
    date = models.DateField()
    balance = models.DecimalField(decimal_places=2, max_digits=40)
    stakeholder = models.ForeignKey(Stakeholder, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date} - {self.stakeholder.name}"


class Expenses(models.Model):
    date = models.DateField()
    amount = models.DecimalField(decimal_places=2, max_digits=40)
    stakeholder = models.ForeignKey(Stakeholder, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date} - {self.stakeholder.name}"

