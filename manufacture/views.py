from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Branch, Service, Order, Status
from users.permissions import IsAdminRole, IsManagerRole, IsPrinterRole, IsFactoryRole



class OrderStatusAutoChange(APIView):
    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        if request.user.role.lower() in ["admin", "manager"]:
            status_obj = Status.objects.get_or_create(name="Pechat")
        elif request.user.role.lower() == "Pechat":
            status_obj = Status.objects.get_or_create(name="Qayta ishlash")
        elif request.user.role.lower() == "qayta ishlash":
            status_obj = Status.objects.get_or_create(name="Final")
        order.status = status_obj
        order.save()
        return Response({"success": True})

