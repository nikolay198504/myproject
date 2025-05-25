from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import uuid
from .models import Order

def calc(request):
    order_id = request.GET.get('order_id')
    return render(request, 'calculator/calc.html', {'order_id': order_id})

def payment_success(request):
    order_id = request.GET.get('order_id')
    return render(request, 'calculator/payment_success.html', {'order_id': order_id})

def create_order(request):
    if request.method == "POST":
        # Можно добавить получение email/phone из POST-данных, если нужно
        order = Order.objects.create(status="pending")
        return JsonResponse({"order_id": order.order_id})
    return JsonResponse({"error": "Only POST allowed"}, status=405)
