# api_service/payments.py

from fastapi import APIRouter, Request, HTTPException, Body
from pydantic import BaseModel
import hmac
import hashlib
from urllib.parse import urlencode
import requests
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, Column, String, Text, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List, Dict, Any, Optional
from api_service.chunks import Chunk
import datetime
import time
import json
import os

router = APIRouter()

SECRET_KEY = "a9bd459647f44aa52ed6841f9ca4bfcf522868648d8673f4f59619f17e728d1a"
PAYFORM_URL = "https://relacionesarmoniosas.payform.ru"

# Простая база заказов в памяти (для теста)
ORDERS = {}

# --- Настройка базы данных (SQLite для теста) ---
Base = declarative_base()
engine = create_engine("sqlite:///orders.db")
SessionLocal = sessionmaker(bind=engine)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String, default="pending")  # pending, paid, failed
    date = Column(String, nullable=True)        # дата рождения
    points = Column(Text, nullable=True)        # points в виде JSON-строки
    amount = Column(String, nullable=True)  # Можно Float, но для SQLite часто используют String
    customer_phone = Column(String, nullable=True)
    customer_email = Column(String, nullable=True)
    paid_at = Column(DateTime, nullable=True)  # дата и время оплаты
    type = Column(String, default="personal")  # personal или compatibility
    compatibility_result = Column(Text, nullable=True)  # <--- Добавить это поле
    personal_result = Column(Text, nullable=True)  # <--- Добавить это поле

    @property
    def order_id(self):
        return f"ORD-{self.id:06d}"

class PendingOrder(Base):
    __tablename__ = "pending_orders"
    id = Column(Integer, primary_key=True)
    order_num = Column(String, unique=True)
    birth_date = Column(String)
    email = Column(String)
    phone = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)
# --- конец настройки БД ---

class PaymentRequest(BaseModel):
    birth_date: str
    email: str
    phone: str
    points: Optional[List[Dict[str, Any]]] = None
    type: Optional[str] = "personal"

def generate_signature(data: dict, secret_key: str) -> str:
    sorted_items = sorted(data.items())
    message = '&'.join(f"{k}={v}" for k, v in sorted_items)
    return hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")
print(f"[PAYMENTS] Using BASE_URL: {BASE_URL}")

@router.post("/payments/create-link")
async def create_payment_link(payment: PaymentRequest):
    import json
    print("[CREATE-LINK] Запрос на создание заказа:", payment)
    print("Создаём заказ с points:", payment.points)
    print("Получены points:", payment.points)
    db = SessionLocal()
    # Получаем тип заказа, если передан, иначе personal
    order_type = getattr(payment, "type", "personal")
    amount = "1500" if order_type == "compatibility" else "1000"
    order = Order(
        status="pending",
        date=payment.birth_date or None,
        points=json.dumps(payment.points) if payment.points else json.dumps([]),
        amount=amount,
        customer_phone=payment.phone,
        customer_email=payment.email,
        type=order_type
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    print(f"[CREATE-LINK] Создан заказ: id={order.id}, order_id={order.order_id}, type={order.type}")
    db.close()
    # Формируем data только для payform.ru!
    data = {
        "amount": amount,
        "order_id": order.order_id,
        "description": f"Заказ №{order.order_id}. Сумма: {amount} руб.",
        "customer_email": payment.email or "",
        "customer_phone": payment.phone or "",
        "success_url": f"{BASE_URL}/?order_id={order.order_id}",
        "fail_url": f"{BASE_URL}/",
        "notification_url": f"{BASE_URL}/api/payments/webhook"
    }
    print("[CREATE-LINK] Данные для Продамус:", data)
    headers = {
        "Authorization": f"Bearer {SECRET_KEY}",
        "Content-Type": "application/json"
    }
    try:
        # Запрос к платёжной системе (payform/prodamus)
        result = requests.post(PAYFORM_URL, data=data)
        if result.status_code == 200:
            payform_data = result.json()
            return {
                "payment_url": payform_data.get("url"),
                "order_id": order.order_id
            }
        else:
            # Даже если платёжка не ответила, верни order_id!
            return {
                "order_id": order.order_id,
                "payment_url": None,
                "error": "Failed to create payment link, use manual link"
            }
    except Exception as e:
        # На всякий случай — тоже верни order_id
        return {
            "order_id": order.order_id,
            "payment_url": None,
            "error": f"Exception: {str(e)}"
        }

@router.get("/payments/status")
async def payment_status(order_id: str):
    db = SessionLocal()
    order = db.query(Order).filter(Order.order_id == order_id).first()
    status = order.status if order else "not_found"
    db.close()
    return {"order_id": order_id, "status": status}

@router.get("/payment-success", response_class=HTMLResponse)
async def payment_success(request: Request):
    # Здесь можно получить параметры заказа, если они передаются
    # order_id = request.query_params.get("order_id")
    # Здесь логика выдачи ответа пользователю
    return """
    <html>
        <head><title>Оплата прошла успешно</title></head>
        <body>
            <h1>Спасибо за оплату!</h1>
            <p>Ваша оплата прошла успешно. Ожидайте результат на почту или в чате.</p>
        </body>
    </html>
    """

chunk = Chunk()

def parse_order_id(order_id_str):
    try:
        return int(order_id_str.replace("ORD-", ""))
    except Exception:
        return None

@router.get("/payments/paid-interpretation")
async def paid_interpretation(order_id: str):
    import json
    print(f"[PAID-INTERPRETATION] Looking for order with ID: {order_id}")
    db = SessionLocal()
    id_int = parse_order_id(order_id)
    print(f"[PAID-INTERPRETATION] Parsed id: {id_int}")
    order = db.query(Order).filter(Order.id == id_int).first()
    if not order:
        print(f"[PAID-INTERPRETATION] Order {order_id} not found in database")
        db.close()
        raise HTTPException(status_code=404, detail="Order not found")
    print(f"[PAID-INTERPRETATION] Found order: id={order.id}, order_id={order.order_id}, status={order.status}")
    if order.status != "paid":
        print(f"[PAID-INTERPRETATION] Order {order_id} is not paid (status: {order.status})")
        db.close()
        return {"error": "Order not paid"}
    points = json.loads(order.points) if order.points else []
    date = order.date
    print(f"[PAID-INTERPRETATION] Generating interpretation for order {order_id} with points: {points}")
    paid_message = await chunk.consult_paid(points=points, date=date)
    print(f"[PAID-INTERPRETATION] Generated message for order {order_id}: {paid_message}")
    db.close()
    return {"message": paid_message}

chunk = Chunk()

def parse_order_id(order_id_str):
    try:
        return int(order_id_str.replace("ORD-", ""))
    except Exception:
        return None

@router.get("/payments/paid-interpretation")
async def paid_interpretation(order_id: str):
    import json
    print(f"[PAID-INTERPRETATION] Looking for order with ID: {order_id}")
    db = SessionLocal()
    id_int = parse_order_id(order_id)
    print(f"[PAID-INTERPRETATION] Parsed id: {id_int}")
    order = db.query(Order).filter(Order.id == id_int).first()
    if not order:
        print(f"[PAID-INTERPRETATION] Order {order_id} not found in database")
        db.close()
        raise HTTPException(status_code=404, detail="Order not found")
    print(f"[PAID-INTERPRETATION] Found order: id={order.id}, order_id={order.order_id}, status={order.status}")
    if order.status != "paid":
        print(f"[PAID-INTERPRETATION] Order {order_id} is not paid (status: {order.status})")
        db.close()
        return {"error": "Order not paid"}
    points = json.loads(order.points) if order.points else []
    date = order.date
    print(f"[PAID-INTERPRETATION] Generating interpretation for order {order_id} with points: {points}")
    paid_message = await chunk.consult_paid(points=points, date=date)
    print(f"[PAID-INTERPRETATION] Generated message for order {order_id}: {paid_message}")
    db.close()
    return {"message": paid_message}

@router.post("/generate_pay_url")
async def generate_pay_url(payment_request: PaymentRequest):
    # URL API Prodamus для создания счета
    api_url = "https://payform.ru/api/v1/invoice"
    
    # Генерация уникального номера заказа
    order_num = f"ORDER-{int(time.time())}"
    
    # Формируем данные для запроса
    payload = {
        "amount": "1000.00",  # Фиксированная сумма
        "order_id": order_num,
        "description": f"Заказ №{order_num}. Анализ чакр.",
        "customer_phone": payment_request.phone,
        "customer_email": payment_request.email,
        "success_url": f"{BASE_URL}/?order_id={order_num}",
        "fail_url": f"{BASE_URL}/fail",
        "notification_url": f"{BASE_URL}/api/payments/webhook"
    }

    headers = {
        "Authorization": f"Bearer {SECRET_KEY}",
        "Content-Type": "application/json"
    }

    try:
        # Отправляем запрос к API Prodamus
        print("Sending request to Prodamus:", payload)
        response = requests.post(api_url, json=payload, headers=headers)
        print("Prodamus response status:", response.status_code)
        print("Prodamus response text:", response.text)

        # Проверяем статус ответа
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Prodamus API error: {response.text}"
            )

        # Пробуем распарсить JSON ответ
        response_data = response.json()

        # Сохраняем информацию о заказе в БД
        db = SessionLocal()
        try:
            pending_order = PendingOrder(
                order_num=order_num,
                birth_date=payment_request.birth_date,
                email=payment_request.email,
                phone=payment_request.phone
            )
            db.add(pending_order)
            db.commit()
        except Exception as e:
            db.rollback()
            print("Database error:", str(e))
            raise HTTPException(
                status_code=500,
                detail="Failed to save order to database"
            )
        finally:
            db.close()

        # Возвращаем URL для оплаты
        return {
            "payment_url": response_data.get("url"),  # API v1 возвращает url, а не payment_url
            "order_num": order_num
        }

    except requests.RequestException as e:
        print("Request failed:", str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Failed to connect to Prodamus: {str(e)}"
        )
    except Exception as e:
        print("Unexpected error:", str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/payments/save-points")
async def save_points(order_id: str = Body(...), points: list = Body(...)):
    db = SessionLocal()
    try:
        id_int = int(order_id.replace("ORD-", ""))
        order = db.query(Order).filter(Order.id == id_int).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        order.points = json.dumps(points)
        db.commit()
        return {"status": "success"}
    finally:
        db.close()

# --- PDF endpoints (personal and compatibility) ---
@router.get("/payments/paid-interpretation-pdf")
async def paid_interpretation_pdf(order_id: str):
    """
    Возвращает PDF-файл с персональной интерпретацией по order_id.
    Не меняет существующую логику: повторно считает текст так же, как текущий
    /payments/paid-interpretation, и формирует PDF.
    """
    from io import BytesIO
    try:
        # Импорты локально, чтобы не менять глобальные зависимости
        from fastapi.responses import StreamingResponse
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import mm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation dependencies missing: {e}")

    # Получаем текст так же, как в paid_interpretation
    import json
    db = SessionLocal()
    try:
        id_int = parse_order_id(order_id)
        order = db.query(Order).filter(Order.id == id_int).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        if order.status != "paid":
            raise HTTPException(status_code=400, detail="Order not paid")
        points = json.loads(order.points) if order.points else []
        text = await chunk.consult_paid(points=points, date=order.date)
    finally:
        db.close()

    # Генерация PDF с корректными переносами и автоматическими разрывами страниц
    buffer = BytesIO()
    margin = 15 * mm
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            leftMargin=margin, rightMargin=margin,
                            topMargin=margin, bottomMargin=margin)
    styles = getSampleStyleSheet()
    body = styles["BodyText"]
    title = styles["Heading3"]
    story = []

    story.append(Paragraph(f"Order: {order_id}", title))
    story.append(Spacer(1, 8))

    # Разбиваем по пустым строкам на абзацы для лучшего форматирования
    paragraphs = str(text).split("\n\n")
    for p in paragraphs:
        # сохраняем разрывы строк внутри абзаца
        p_html = "<br/>".join(p.splitlines())
        story.append(Paragraph(p_html, body))
        story.append(Spacer(1, 6))

    doc.build(story)
    buffer.seek(0)

    headers = {
        "Content-Disposition": f"attachment; filename={order_id}-personal.pdf"
    }
    return StreamingResponse(buffer, media_type="application/pdf", headers=headers)


@router.get("/payments/compatibility-interpretation-pdf")
async def compatibility_interpretation_pdf(order_id: str):
    """
    Возвращает PDF-файл с интерпретацией совместимости по order_id.
    Берёт сохранённый compatibility_result из БД. Если результата нет — 202.
    """
    from io import BytesIO
    try:
        from fastapi.responses import StreamingResponse
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import mm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation dependencies missing: {e}")

    db = SessionLocal()
    try:
        id_int = parse_order_id(order_id)
        order = db.query(Order).filter(Order.id == id_int).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        if order.type != "compatibility":
            raise HTTPException(status_code=400, detail="Order is not compatibility type")
        if not order.compatibility_result:
            # Результат ещё не готов
            raise HTTPException(status_code=202, detail="Result not ready yet")
        text = order.compatibility_result
    finally:
        db.close()

    # Генерация PDF с переносами и пагинацией
    buffer = BytesIO()
    margin = 15 * mm
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            leftMargin=margin, rightMargin=margin,
                            topMargin=margin, bottomMargin=margin)
    styles = getSampleStyleSheet()
    body = styles["BodyText"]
    title = styles["Heading3"]
    story = []

    story.append(Paragraph(f"Order: {order_id}", title))
    story.append(Spacer(1, 8))

    paragraphs = str(text).split("\n\n")
    for p in paragraphs:
        p_html = "<br/>".join(p.splitlines())
        story.append(Paragraph(p_html, body))
        story.append(Spacer(1, 6))

    doc.build(story)
    buffer.seek(0)

    headers = {
        "Content-Disposition": f"attachment; filename={order_id}-compatibility.pdf"
    }
    return StreamingResponse(buffer, media_type="application/pdf", headers=headers)