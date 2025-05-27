# Отчет по интеграции оплаты и анализу чакр

## 1. Автоматический переход на оплату (без короткой ссылки)

**Что было:**
- После создания заказа пользователь попадал на промежуточную страницу с короткой ссылкой.
- Иногда требовалось вручную кликать по короткой ссылке.

**Что сделали:**
- Используем параметр `do=pay` вместо `do=link` в ссылке оплаты.
- Передаем email или телефон пользователя обязательно (иначе мгновенный переход невозможен).

**Фрагмент JS:**
```js
let payUrl = `https://relacionesarmoniosas.payform.ru/?products[0][price]=1000&products[0][quantity]=1&products[0][name]=Чакры&order_id=${orderId}`;
if (email) payUrl += `&customer_email=${encodeURIComponent(email)}`;
if (phone) payUrl += `&customer_phone=${encodeURIComponent(phone)}`;
payUrl += `&do=pay`;
window.location.href = payUrl;
```

---

## 2. Сохранение points на backend при создании заказа

**Что было:**
- Points (данные для анализа чакр) хранились только в localStorage браузера.
- После оплаты, если localStorage был пустой (другой браузер, вкладка, устройство) — результат не появлялся.

**Что сделали:**
- При нажатии "Да" points отправляются на backend вместе с email/телефоном при создании заказа.

**Фрагмент JS:**
```js
const points = getPaidPoints();
const response = await fetch('/create_order/', {
    method: "POST",
    headers: {
        "X-CSRFToken": window.CSRF_TOKEN,
        "Content-Type": "application/json"
    },
    body: JSON.stringify({ email, phone, points })
});
```

---

## 3. Сохранение points в заказе (backend)

**Что было:**
- В базе points были пустыми или не сохранялись вовсе.

**Что сделали:**
- Backend (FastAPI/Django) сохраняет points в заказе (в поле points, как JSON).

**Фрагмент FastAPI:**
```python
class PaymentRequest(BaseModel):
    birth_date: str
    email: str
    phone: str
    points: Optional[List[Dict[str, Any]]] = None

@router.post("/payments/create-link")
async def create_payment_link(payment: PaymentRequest):
    print("Получены points:", payment.points)
    db = SessionLocal()
    order = Order(
        status="pending",
        date=payment.birth_date or datetime.date.today().isoformat(),
        points=json.dumps(payment.points) if payment.points else json.dumps([]),
        amount="1000",
        customer_phone=payment.phone,
        customer_email=payment.email
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    db.close()
    # ...
```

---

## 4. Webhook: обновление статуса заказа

**Что было:**
- После оплаты статус заказа не всегда обновлялся.

**Что сделали:**
- Webhook от Prodamus меняет статус заказа на `paid` после успешной оплаты.

**Фрагмент:**
```python
if payment_status == "success" and (order_num or payform_order_id):
    # ...
    order.status = "paid"
    order.paid_at = datetime.datetime.now()
    db.commit()
```

---

## 5. Гарантированный вывод результата по чакрам после оплаты

**Что было:**
- После оплаты результат появлялся только если points были в localStorage.

**Что сделали:**
- После оплаты JS-код делает запрос на `/api/payments/paid-interpretation?order_id=...`.
- Backend достаёт points из заказа и возвращает расширенную интерпретацию по чакрам.

**Фрагмент JS:**
```js
fetch(`/api/payments/paid-interpretation?order_id=${orderId}`)
  .then(response => response.json())
  .then(data => {
    if (data.message) {
      addBotMessage("Спасибо за оплату! Вот твой результат по чакрам:\n" + data.message);
    } else {
      addBotMessage("Не удалось получить результат. Попробуйте позже.");
    }
  });
```

**Фрагмент FastAPI:**
```python
@router.get("/payments/paid-interpretation")
async def paid_interpretation(order_id: str):
    order = db.query(Order).filter(Order.id == id_int).first()
    if not order or order.status != "paid":
        return {"error": "Order not paid"}
    points = json.loads(order.points) if order.points else []
    paid_message = await chunk.consult_paid(points=points, date=order.date)
    return {"message": paid_message}
```

---

## 6. Ключевые моменты
- Переход на оплату теперь мгновенный (без промежуточной короткой ссылки), если указан email или телефон и do=pay.
- Points всегда сохраняются на backend при создании заказа.
- После оплаты результат по чакрам появляется всегда, даже если localStorage пустой.
- Вся логика теперь не зависит от localStorage пользователя.

---

**Теперь система оплаты и анализа чакр работает надёжно и предсказуемо!** 