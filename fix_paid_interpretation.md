# Исправление отображения платной интерпретации по чакрам в чат-боте

## Проблема

После оплаты заказ появлялся в базе со статусом `paid`, но результат по чакрам не отображался в чат-боте, если points отсутствовали в localStorage (например, при возврате пользователя по ссылке с order_id).

## Причина

Вызов функции `pollPaidInterpretation(orderId)` происходил только если в localStorage были points:

```js
if (orderId && points.length && points.some(p => p.value > 0)) {
  savePaidPoints(orderId, points);
  pollPaidInterpretation(orderId);
  localStorage.removeItem("paidPoints");
}
```

Если points не было — бот не опрашивал сервер и не показывал результат.

## Решение

Добавили дополнительный вызов `pollPaidInterpretation(orderId)` при наличии orderId, даже если points нет в localStorage:

```js
if (orderId && points.length && points.some(p => p.value > 0)) {
  savePaidPoints(orderId, points);
  pollPaidInterpretation(orderId);
  localStorage.removeItem("paidPoints");
} else if (orderId) {
  pollPaidInterpretation(orderId);
}
```

## Результат

Теперь бот всегда опрашивает сервер и показывает результат по чакрам, если заказ оплачен и есть в базе, даже после обновления страницы или перехода по ссылке с order_id. 