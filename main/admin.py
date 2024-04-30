from django.contrib import admin
from .models import Branch, Status, Product, Inventory, Size, Customer, Order, Service, InventoryOrder, ServiceOrder, Purchase, CustomerDebt, OrderPayment, Debt, CustomUser

# Register your models here.
admin.site.register(Branch)
admin.site.register(Status)
admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(Size)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Service)
admin.site.register(InventoryOrder)
admin.site.register(ServiceOrder)
admin.site.register(Purchase)
admin.site.register(CustomerDebt)
admin.site.register(OrderPayment)
admin.site.register(Debt)
admin.site.register(CustomUser)
