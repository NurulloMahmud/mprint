from django.contrib import admin
from .models import (
    Branch, Status, Paper, Customer, OrderPics,
    Order, Service, ServiceOrder, CustomerDebt, 
    OrderPayment, CustomUser, PaperType, PaymentMethod,
)

# Register your models here.
admin.site.register(Branch)
admin.site.register(Status)
admin.site.register(Paper)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Service)
admin.site.register(ServiceOrder)
admin.site.register(CustomerDebt)
admin.site.register(OrderPayment)
admin.site.register(CustomUser)
admin.site.register(PaperType)
admin.site.register(OrderPics)
admin.site.register(PaymentMethod)