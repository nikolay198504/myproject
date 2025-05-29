from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import uuid
from .models import Order
import json

def calc(request):
    order_id = request.GET.get('order_id')
    return render(request, 'calculator/calc.html', {'order_id': order_id})

def payment_success(request):
    order_id = request.GET.get('order_id')
    return render(request, 'calculator/payment_success.html', {'order_id': order_id})

def create_order(request):
    if request.method == "POST":
        data = json.loads(request.body)
        order = Order.objects.create(
            status="pending",
            date=data.get("birth_date"),
            customer_email=data.get("email"),
            customer_phone=data.get("phone"),
        )
        return JsonResponse({"order_id": order.order_id})
    return JsonResponse({"error": "Only POST allowed"}, status=405)