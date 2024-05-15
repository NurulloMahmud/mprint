from django.db import models
from django.contrib.auth.models import AbstractUser


class Branch(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class PaperType(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.name


class CustomUser(AbstractUser):
    role = models.CharField(
        max_length=50, null=True, blank=True
    )
    is_active = models.BooleanField(default=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.branch:  # Check if branch is not set
            branch, created = Branch.objects.get_or_create(name='Andijon')  # Create Andijon branch if not exists
            self.branch = branch
        super().save(*args, **kwargs)


class Status(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Paper(models.Model):
    name = models.CharField(max_length=100)
    paper_type = models.ForeignKey(PaperType, on_delete=models.CASCADE, null=True, blank=True)
    grammaj = models.CharField(max_length=250, null=True, blank=True)
    cost = models.DecimalField(decimal_places=2, max_digits=10)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    available_qty = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    telegram_id = models.BigIntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=500)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products_qty = models.IntegerField(null=True, blank=True)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, null=True, blank=True)
    num_of_lists = models.IntegerField(null=True, blank=True)
    total_sqr_meter = models.FloatField(null=True, blank=True)
    possible_defect_list = models.IntegerField(null=True, blank=True)
    price_per_list = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    total_price = models.DecimalField(decimal_places=2, max_digits=10)
    final_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    price_per_product = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    num_of_product_per_list = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # If the order is being created (not updated)
            pending_status = Status.objects.get(name="Pending")
            self.status = pending_status
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class OrderPics(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="pics")
    pic = models.ImageField()

    def __str__(self) -> str:
        return self.order.name


class Service(models.Model):
    name = models.CharField(max_length=100)
    price_per_sqr = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    price_per_qty = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    minimum_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class ServiceOrder(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    total_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # If the order is being created (not updated)
            if self.total_price < self.service.minimum_price:
                self.total_price = self.service.minimum_price
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.service.name


class Purchase(models.Model):
    date = models.DateField(auto_now_add=True)
    item = models.CharField(max_length=200)
    unit_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    total_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.item


class CustomerDebt(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    last_update = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.customer.name


class OrderPayment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.order.name


class Debt(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self) -> str:
        return self.purchase.item


class Inventory(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(decimal_places=2, max_digits=10)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    available = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name

