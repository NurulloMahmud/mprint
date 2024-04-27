from django.db import models


class Paper(models.Model):
    name = models.CharField(max_length=100)
    weight = models.FloatField()
    cost = models.DecimalField(decimal_places=2, max_digits=10)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self) -> str:
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=100)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

