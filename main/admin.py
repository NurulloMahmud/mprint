from django.contrib import admin
from .models import Branch, Status, Paper, Customer, Order, Service, ServiceOrder, Purchase, CustomerDebt, OrderPayment, Debt, CustomUser, PaperType

# Register your models here.
admin.site.register(Branch)
admin.site.register(Status)
admin.site.register(Paper)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Service)
admin.site.register(ServiceOrder)
admin.site.register(Purchase)
admin.site.register(CustomerDebt)
admin.site.register(OrderPayment)
admin.site.register(Debt)
admin.site.register(CustomUser)
admin.site.register(PaperType)
