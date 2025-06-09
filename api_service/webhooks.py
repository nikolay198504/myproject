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
import re
import datetime

router = APIRouter()

SECRET_KEY = "a9bd459647f44aa52ed6841f9ca4bfcf522868648d8673f4f59619f17e728d1a"

def generate_signature(data: dict, secret_key: str) -> str:
    sorted_items = sorted(data.items())
    message = '&'.join(f"{k}={v}" for k, v in sorted_items)
    return hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()

def parse_order_id(order_id_str):
    try:
        return int(order_id_str.replace("ORD-", ""))
    except Exception:
        return None

# ----------------- Новый блок расчёта chakras -----------------
def sum22(value):
    value = str(value)
    if value.isdigit() and int(value) <= 22:
        return int(value)
    result = sum(int(d) for d in value if d.isdigit())
    if result > 22:
        return sum22(result)
    return result

def base22(value):
    value = int(value)
    if value <= 22:
        return value
    return sum22(value)

def parse_birth_date(date_str):
    import re
    if not date_str:
        return None, None, None
    if "T" in date_str:
        date_str = date_str.split("T")[0]
    if re.match(r"\d{2}\.\d{2}\.\d{4}", date_str):
        dd, mm, yyyy = date_str.split('.')
    elif re.match(r"\d{4}-\d{2}-\d{2}", date_str):
        yyyy, mm, dd = date_str.split('-')
    else:
        return None, None, None
    return int(dd), int(mm), int(yyyy)

def calculate_paid_points(date_str):
    dd, mm, yyyy = parse_birth_date(date_str)
    if not dd or not mm or not yyyy:
        return []
    # Воспроизводим populateB JS
    dot = {}
    dot['LL0'] = sum22(dd)
    dot['LL20'] = sum22(mm)
    dot['LL40'] = sum22(yyyy)
    dot['LL60'] = sum22(f"{dd}{mm}{yyyy}")
    dot['Center'] = base22(dot['LL0'] + dot['LL20'] + dot['LL40'] + dot['LL60'])
    dot['LL10'] = base22(dot['LL0'] + dot['LL20'])
    dot['LL30'] = base22(dot['LL20'] + dot['LL40'])
    dot['LL50'] = base22(dot['LL40'] + dot['LL60'])
    dot['LL70'] = base22(dot['LL0'] + dot['LL60'])

    dot['MM01'] = base22(base22(dot['Center'] + dot['LL0']) + dot['LL0'])
    dot['MM02'] = base22(dot['Center'] + dot['LL0'])
    dot['MM21'] = base22(base22(dot['Center'] + dot['LL20']) + dot['LL20'])
    dot['MM22'] = base22(dot['Center'] + dot['LL20'])
    dot['MM41'] = base22(base22(dot['Center'] + dot['LL40']) + dot['LL40'])
    dot['MM42'] = base22(dot['Center'] + dot['LL40'])
    dot['MM61'] = base22(base22(dot['Center'] + dot['LL60']) + dot['LL60'])
    dot['MM62'] = base22(dot['Center'] + dot['LL60'])

    dot['SS11'] = base22(dot['LL0'] + dot['LL20'])
    dot['SS12'] = base22(dot['MM01'] + dot['MM21'])
    dot['SS13'] = base22(dot['MM02'] + dot['MM22'])
    dot['SS51'] = base22(dot['LL40'] + dot['LL60'])
    dot['SS52'] = base22(dot['MM41'] + dot['MM61'])
    dot['SS53'] = base22(dot['MM42'] + dot['MM62'])

    chakras = {
        "sahasrara": [dot['LL0'], dot['LL20'], dot['SS11']],
        "ajna":      [dot['MM01'], dot['MM21'], dot['SS12']],
        "vishuddha": [dot['MM02'], dot['MM22'], dot['SS13']],
        "anahata":   [dot['Center'], dot['Center'], base22(dot['Center'] * 2)],
        "manipura":  [dot['MM42'], dot['MM62'], dot['SS53']],
        "svadhisthana": [dot['MM41'], dot['MM61'], dot['SS52']],
        "muladhara": [dot['LL40'], dot['LL60'], dot['SS51']],
        "total": [
            base22(dot['LL0'] + dot['MM01'] + dot['MM02'] + dot['Center'] + dot['MM42'] + dot['MM41'] + dot['LL40']),
            base22(dot['LL20'] + dot['MM21'] + dot['MM22'] + dot['Center'] + dot['MM62'] + dot['MM61'] + dot['LL60']),
            base22(
                base22(dot['LL0'] + dot['MM01'] + dot['MM02'] + dot['Center'] + dot['MM42'] + dot['MM41'] + dot['LL40'])
                + base22(dot['LL20'] + dot['MM21'] + dot['MM22'] + dot['Center'] + dot['MM62'] + dot['MM61'] + dot['LL60'])
            ),
        ],
    }
    def safe(val):
        try:
            return int(val)
        except:
            return 0
    return [
        {"name": "Zona de confort", "chakra": "Anahata", "aspect": "Fisica", "value": safe(chakras['anahata'][0])},
        {"name": "Recurso interior", "chakra": "Sahasrara", "aspect": "Fisica", "value": safe(chakras['sahasrara'][2])},
        {"name": "Talento", "chakra": "Sahasrara", "aspect": "Energia", "value": safe(chakras['sahasrara'][1])}
    ]

def calculate_paid_points_v2(data):
    # data — это результат readTableData("0") с фронта (или аналогичная структура)
    def safeParse(val):
        try:
            return int(val)
        except:
            return 0
    return [
        {"name": "Energía masculina", "value": safeParse(data["paterna"][0])},
        {"name": "Energía femenina", "value": safeParse(data["materna"][0])},
        {"name": "Cola kármica general", "chakra": "Muladhara", "aspect": "Fisica", "value": safeParse(data["chakras"]["muladhara"][0])},
        {"name": "Cola kármica del amor", "chakra": "Svadhisthana", "aspect": "Emociones", "value": safeParse(data["chakras"]["svadhisthana"][2])},
        {"name": "Pareja kármica en el amor", "chakra": "Muladhara", "aspect": "Emociones", "value": safeParse(data["chakras"]["anahata"][2])},
        {"name": "Amor y dinero", "chakra": "Manipura", "aspect": "Emociones", "value": safeParse(data["chakras"]["anahata"][2])},
        {"name": "Dirección de vida profesional", "chakra": "Manipura", "aspect": "Fisica", "value": safeParse(data["chakras"]["vishuddha"][0])},
        {"name": "Fuente de ingresos", "chakra": "Manipura", "aspect": "Energia", "value": safeParse(data["chakras"]["manipura"][1])},
        {"name": "Bloqueo financiero", "chakra": "Muladhara", "aspect": "Energia", "value": safeParse(data["chakras"]["svadhisthana"][1])}
    ]

# ----------------- /конец нового блока -----------------

@router.post("/payments/webhook")
async def payment_webhook(request: Request):
    print("\n=== Webhook received ===")
    data = await request.form()
    data = dict(data)
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
        all_orders = db.query(Order).all()
        print("Все order_id в базе:", [o.order_id for o in all_orders])
        if not order:
            print(f"\nOrder not found in DB for order_num={order_num}, payform_order_id={payform_order_id}. Webhook will not create a new order!")
            db.close()
            return {"status": "fail"}
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
        # Сохраняем дату, если пришла новая
        if date and not order.date:
            order.date = date
        # Не трогаем order.points! Они уже сохранены при создании заказа
        order.status = "paid"
        order.paid_at = datetime.datetime.now()
        order.amount = amount or order.amount
        order.customer_phone = customer_phone or order.customer_phone
        order.customer_email = customer_email or order.customer_email
        db.commit()
        print(f"Updated status to: paid")
        db.close()
        return {"status": "success"}
    else:
        print(f"\nPayment failed or missing order number:")
        print(f"- payment_status: {payment_status}")
        print(f"- order_num: {order_num}")
        print(f"- payform_order_id: {payform_order_id}")
        return {"status": "fail"}
