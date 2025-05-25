"""
api_service/webhooks.py

Этот файл содержит обработчик webhook (уведомлений) от платёжной системы Продамус.
Webhook вызывается Продамус после успешной оплаты, чтобы уведомить ваш backend о статусе заказа.

Что делает этот файл:
- Принимает POST-запросы от Продамус на специальный endpoint.
- Проверяет подпись (signature) для безопасности, чтобы убедиться, что уведомление пришло именно от Продамус.
- Если подпись верна — отмечает заказ как оплаченный (здесь можно добавить обновление статуса заказа в БД).
- Возвращает ответ Продамус ("success"), чтобы подтвердить приём уведомления.
"""

from fastapi import APIRouter, Request, HTTPException, Form
import hmac
import hashlib
import json
from api_service.payments import ORDERS, SessionLocal, Order, PendingOrder
# from api_service.calc import calculate_chakras_from_date
import re
import datetime

router = APIRouter()

# Секретный ключ должен совпадать с тем, что используется для генерации платёжной ссылки
SECRET_KEY = "a9bd459647f44aa52ed6841f9ca4bfcf522868648d8673f4f59619f17e728d1a"

# Функция для генерации подписи (signature) на основе данных и секретного ключа
# Используется для проверки, что уведомление действительно пришло от Продамус
def generate_signature(data: dict, secret_key: str) -> str:
    sorted_items = sorted(data.items())
    message = '&'.join(f"{k}={v}" for k, v in sorted_items)
    return hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()

def parse_order_id(order_id_str):
    try:
        return int(order_id_str.replace("ORD-", ""))
    except Exception:
        return None

@router.post("/payments/webhook")
async def payment_webhook(request: Request):
    print("\n=== Webhook received ===")
    print("Request headers:", dict(request.headers))
    data = await request.form()
    data = dict(data)
    print("Raw form data:", data)
    order_num = data.get("order_num")
    payform_order_id = data.get("_payform_order_id")
    payment_status = data.get("payment_status")
    amount = data.get("sum")
    customer_phone = data.get("customer_phone")
    customer_email = data.get("customer_email")
    date = data.get("date")
    print(f"\nParsed webhook data:")
    print(f"- order_num: {order_num}")
    print(f"- payform_order_id: {payform_order_id}")
    print(f"- payment_status: {payment_status}")
    print(f"- amount: {amount}")
    print(f"- customer_phone: {customer_phone}")
    print(f"- customer_email: {customer_email}")
    print(f"- date: {date}")
    if payment_status == "success" and (order_num or payform_order_id):
        db = SessionLocal()
        id_int = parse_order_id(order_num)
        order = db.query(Order).filter(Order.id == id_int).first()
        if not order:
            pending = db.query(PendingOrder).filter(PendingOrder.order_num == order_num).first()
            birth_date = pending.birth_date if pending else None
            order = Order(
                status="pending",
                amount=amount,
                customer_phone=customer_phone,
                customer_email=customer_email,
                date=birth_date,
            )
            db.add(order)
            db.commit()
            db.refresh(order)
        if order:
            print(f"\nFound order in database:")
            print(f"- order_id: {order.order_id}")
            print(f"- current status: {order.status}")
            print(f"- amount: {order.amount}")
            print(f"- date: {order.date}")
            if order.date:
                date_str = order.date
                print(f"order.date: {date_str}")
                match = re.match(r"(\d{4})-(\d{2})-(\d{2})", date_str)
                if match:
                    date_for_calc = f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
                else:
                    match = re.match(r"(\d{2})\.(\d{2})\.(\d{4})", date_str)
                    if match:
                        date_for_calc = f"{match.group(3)}-{match.group(2)}-{match.group(1)}"
                    else:
                        print(f"Неизвестный формат даты: {date_str}")
                        date_for_calc = None
                print(f"date_for_calc: {date_for_calc}")
                if date_for_calc:
                    print("Расчёт чакр на сервере отключён (нет функции calculate_chakras_from_date).")
                else:
                    print("Не удалось определить дату для расчёта чакр!")
            # Сохраняем дату, если пришла новая
            if date and not order.date:
                order.date = date
            # Сохраняем points, если умеете их вычислять
            # order.points = calculate_points_from_date(date)
            order.status = "paid"
            order.paid_at = datetime.datetime.now()
            order.amount = amount or order.amount
            order.customer_phone = customer_phone or order.customer_phone
            order.customer_email = customer_email or order.customer_email
            db.commit()
            print(f"Updated status to: paid")
            if order.points:
                print(f"Updated points: {order.points}")
        else:
            print(f"\nOrder not found in database! Searched for:")
            print(f"- order_num: {order_num}")
            print(f"- payform_order_id: {payform_order_id}")
        db.close()
        return {"status": "success"}
    else:
        print(f"\nPayment failed or missing order number:")
        print(f"- payment_status: {payment_status}")
        print(f"- order_num: {order_num}")
        print(f"- payform_order_id: {payform_order_id}")
        return {"status": "fail"}
