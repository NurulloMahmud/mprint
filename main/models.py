from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from decimal import Decimal
from django.core.exceptions import ValidationError
import math
from django.db.models import Sum
from main.bot import send_telegram_message



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
    paper_type = models.ForeignKey(PaperType, on_delete=models.CASCADE, null=True, blank=True)
    grammaj = models.CharField(max_length=250, null=True, blank=True)
    cost = models.DecimalField(decimal_places=2, max_digits=40)
    price = models.DecimalField(decimal_places=2, max_digits=40)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    available_qty = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.grammaj


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
    price_per_list = models.DecimalField(decimal_places=2, max_digits=40, null=True, blank=True)
    total_price = models.DecimalField(decimal_places=2, max_digits=40)
    final_price = models.DecimalField(decimal_places=2, max_digits=40, null=True, blank=True)
    price_per_product = models.DecimalField(decimal_places=2, max_digits=40, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='orders')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    num_of_product_per_list = models.IntegerField(null=True, blank=True)
    lists_per_paper = models.IntegerField(null=True, blank=True)
    special_service_name = models.CharField(max_length=100, null=True, blank=True)
    special_service_amount = models.DecimalField(decimal_places=2, max_digits=40, null=True, blank=True, default=0)

    def save(self, *args, **kwargs):
        if not self.pk:  # If the order is being created (not updated)
            pending_status = Status.objects.get(name="Kutishda")
            self.status = pending_status
        else:
            obj = Order.objects.get(pk=self.pk)
            if self.status.name.lower() == "pending" and obj.status.name.lower() in ["completed", "review"]:
                raise ValidationError("Order cannot be updated")
            
            # add debt to customer if order is finished
            # if order in finished status is being updated, delete debt from customer
            if obj.status.name != "mijoz olib ketdi" and self.status.name == "mijoz olib ketdi":
                total_paid = OrderPayment.objects.filter(order=self).aggregate(Sum('amount'))['amount__sum'] or 0
                if total_paid < self.final_price:
                    CustomerDebt.objects.create(order=self, amount=self.final_price - total_paid, customer=self.customer)
            elif obj.status.name == "mijoz olib ketdi" and self.status.name != "mijoz olib ketdi":
                CustomerDebt.objects.filter(order=self).delete()

        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.status.name != 'Kutishda':
            raise ValidationError('Order cannot be deleted')
        else:
            num_of_lists = int(self.num_of_lists or 0)
            possible_defect_list = int(self.possible_defect_list or 0)
            lists_per_paper = int(self.lists_per_paper or 0)
            self.paper.available_qty += math.ceil((num_of_lists + possible_defect_list) / lists_per_paper)
            self.paper.save()
            super().delete(*args, **kwargs)
    
    def calculate(self, service_ids):
        total_service_price = Decimal(0)
        
        # Calculate paper price
        if self.products_qty and self.paper and self.paper.price \
            and self.num_of_product_per_list and self.lists_per_paper:
            total_num_of_lists = int(self.products_qty) / int(self.num_of_product_per_list) + int(self.possible_defect_list or 0)
            num_of_lists_used = int(self.products_qty) / int(self.num_of_product_per_list)
            num_of_lists_used = math.ceil(num_of_lists_used)
            num_of_lists_used = int(num_of_lists_used)
            total_num_of_lists = int(total_num_of_lists)
            num_of_papers_used = total_num_of_lists / int(self.lists_per_paper)
            num_of_papers_used = math.ceil(num_of_papers_used)

            # add the paper price to total and calculate number of lists used
            total = num_of_papers_used * Decimal(self.paper.price)
            total_paper_price = Decimal(total)
            self.num_of_lists = num_of_lists_used
            self.total_price = total_paper_price
            self.save()

            # minus number of papers from paper's quantity
            self.paper.available_qty -= num_of_papers_used
            self.paper.save()

            # add paper price to paper expenses
            from accounting.models import PaperExpenses
            PaperExpenses.objects.create(
                paper=self.paper,
                quantity=num_of_papers_used,
                order=self
            )
        else:
            total_paper_price = Decimal(0)
        
        # Create ServiceOrder instances and calculate total service price
        for service_id in service_ids:
            service_obj = Service.objects.get(id=service_id)
            service_order = ServiceOrder.objects.create(
                service=service_obj,
                order=self,
            )
            total_service_price += service_order.total_price
        
        self.total_price = total_service_price + total_paper_price
        self.price_per_list = self.final_price / int(self.num_of_lists) if self.num_of_lists else Decimal(0)
        self.price_per_product = self.final_price / int(self.products_qty) if self.products_qty else Decimal(0)
        self.total_price += Decimal(self.special_service_amount)
        self.save()

    def __str__(self):
        return self.name


class OrderPics(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="pics")
    pic = models.ImageField()

    def __str__(self) -> str:
        return self.order.name


class Service(models.Model):
    name = models.CharField(max_length=100)
    price_per_sqr = models.DecimalField(decimal_places=2, max_digits=40, null=True, blank=True)
    price_per_qty = models.DecimalField(decimal_places=2, max_digits=40, null=True, blank=True)
    minimum_price = models.DecimalField(decimal_places=2, max_digits=40, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class ServiceOrder(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='services')
    total_price = models.DecimalField(decimal_places=2, max_digits=40, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # If the order is being created (not updated)
            if self.service.price_per_sqr is not None:
                self.total_price = Decimal(self.order.total_sqr_meter) * Decimal(self.service.price_per_sqr)
            if self.service.price_per_qty is not None:
                self.total_price = self.order.num_of_lists * self.service.price_per_qty
            
            if self.total_price < self.service.minimum_price:
                self.total_price = self.service.minimum_price

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.service.name


class CustomerDebt(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='debt')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="debt")
    amount = models.DecimalField(decimal_places=2, max_digits=40)
    last_update = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.customer.name


class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class OrderPayment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(decimal_places=2, max_digits=40)
    date = models.DateField(auto_now_add=True)
    method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.order.name
    
    def save(self, *args, **kwargs):
        with transaction.atomic():
            if not self.pk:  # If the order is being created (not updated)
                if self.amount > self.order.final_price:
                    raise ValidationError("To'lov miqdori to'g'ri emas")
                if not CustomerDebt.objects.filter(order=self.order).exists():
                    raise ValidationError("Ushbu buyurtmaning qarzi yo'q")
                total_paid = OrderPayment.objects.filter(order=self.order).aggregate(Sum('amount'))['amount__sum'] or 0
                customer_debt = CustomerDebt.objects.get(order=self.order)
                if total_paid + self.amount > self.order.final_price:
                    raise ValidationError("Ushbu to'lov qarz miqdoridan ko'p")
                if self.amount < 0:
                    raise ValidationError("To'lov miqdori to'g'ri emas")
                customer_debt.amount -= self.amount
                customer_debt.save()

                # send telegram message
                if self.order.customer.telegram_id:
                    text = f"Assalomu aleykum\n{self.order.id} raqarmli buyurtmangiz uchun to'lov qabul qilindi\nBuyurtma nomi: {self.order.name}\nTo'langan summa: {self.amount}\nBuyurtmadan qolgan qarzingiz: {customer_debt.amount}"
                    try:
                        send_telegram_message(text, self.order.customer.telegram_id)
                        text += f"\nBuyurtmachi: {self.order.customer.name}"
                        send_telegram_message(text, 5769837552)
                    except:
                        pass
            else:
                total_paid = OrderPayment.objects.filter(order=self.order).aggregate(Sum('amount'))['amount__sum'] or 0
                if total_paid + self.amount > self.order.final_price:
                    raise ValidationError("Ushbu to'lov qarz miqdoridan ko'p")
                if self.amount < 0:
                    raise ValidationError("To'lov miqdori to'g'ri emas")
                customer_debt = CustomerDebt.objects.get(order=self.order)
                total_amount_paid = OrderPayment.objects.filter(order=self.order).aggregate(Sum('amount'))['amount__sum'] or 0
                total_paid = total_amount_paid + self.amount
                if total_paid > customer_debt.amount:
                    raise ValueError("Ushbu to'lov qarz miqdoridan ko'p")
                customer_debt.amount -= self.amount
                customer_debt.save()
                
            super().save(*args, **kwargs)


class Inventory(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(decimal_places=2, max_digits=40)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    available = models.IntegerField(default=0)
    total_price = models.DecimalField(decimal_places=2, max_digits=40, default=0)

    def save(self, *args, **kwargs):
        self.total_price = self.cost * int(self.available or 0)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class OrderManager(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_manager")
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="order_manager")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.order.name} >>> {self.manager.username}"
