from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Branch, Service, Order
from users.permissions import IsAdminRole, IsManagerRole, IsPrinterRole, IsFactoryRole



