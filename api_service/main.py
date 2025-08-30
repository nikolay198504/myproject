from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from api_service.chunks import Chunk
import json
import os
import traceback
from fastapi import FastAPI
from api_service.payments import router as payments_router, PendingOrder, SessionLocal, Order
from api_service.webhooks import router as webhooks_router
import random
import datetime
from starlette.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))

app = FastAPI(
    title="Нейро-консультант API",
    version="1.0.0",
    description="API для получения ответов нейро-консультанта матрицы судьбы"
)

# Монтируем статику из calculator/static
app.mount(
    "/static",
    StaticFiles(directory=os.path.join("calculator", "static")),
    name="static"
)

# Подключаем роутеры
app.include_router(payments_router)
app.include_router(webhooks_router)


# Определяем класс FreePoint для бесплатных точек
class FreePoint(BaseModel):
    chakra: str
    aspect: str
    value: int

# Модель для бесплатной интерпретации
class ModelPersonal(BaseModel):
    free_points: List[FreePoint]

# Модель для платных точек
class PaidPoint(BaseModel):
    name: str
    chakra: str
    aspect: str
    value: int

class ModelPaid(BaseModel):
    points: List[PaidPoint]
    date: str = None

class ModelAnswer(BaseModel):
    text: str

class ModelCompatibility(BaseModel):
    partner1: dict
    partner2: dict

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

request_count = 0
chunk = Chunk()

# --- Загрузка правил из Rules.json ---
RULES_PATH = os.path.join(os.path.dirname(__file__), './base/Rules.json')
with open(RULES_PATH, encoding='utf-8') as f:
    RULES = json.load(f)

@app.post("/consult_personal")
async def consult_personal(data: ModelPersonal):
    try:
        if not data.free_points or not isinstance(data.free_points, list):
            raise ValueError("Некорректные данные: 'free_points' отсутствует или это не список")
        for point in data.free_points:
            if not all(getattr(point, key, None) is not None for key in ["chakra", "aspect", "value"]):
                raise ValueError(f"Некорректная точка: {point}")
        answer = await chunk.consult_personal([p.dict() for p in data.free_points])
        return {"message": answer}
    except ValueError as ve:
        return JSONResponse(status_code=400, content={"error": str(ve)})
    except Exception as e:
        print("Ошибка в обработчике /consult_personal:", e)
        print(traceback.format_exc())
        return JSONResponse(status_code=500, content={"error": "Произошла ошибка на сервере"})

@app.post("/consult_paid")
async def consult_paid(data: ModelPaid):
    try:
        result = await chunk.consult_paid(
            points=[p.dict() for p in data.points],
            date=data.date
        )
        return {"message": result}
    except Exception as e:
        print("Ошибка в обработчике /consult_paid:", e)
        print(traceback.format_exc())
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/consult_compatibility")
async def consult_compatibility(data: ModelCompatibility):
    try:
        # На первом этапе всегда возвращаем предложение оплатить (испанский текст для чата)
        return {"message": "🔮 ¿Quieres descubrir tu compatibilidad con otra persona? (premium)"}
    except Exception as e:
        print("Ошибка в обработчике /consult_compatibility:", e)
        print(traceback.format_exc())
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/get_answer_async")
async def get_answer_async(data: ModelAnswer):
    try:
        answer = await chunk.get_answer_async(data.text)
        return {"message": answer}
    except Exception as e:
        print("Ошибка в обработчике /get_answer_async:", e)
        print(traceback.format_exc())
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/request_count")
def get_request_count():
    return {"request_count": request_count}

@app.get("/get_rules")
async def get_rules():
    try:
        # Пример возврата статичных данных для теста
        return {
            "energy1": {
                "name": "Огонь",
                "desc": "Энергия страсти и решительности..."
            },
            "energy2": {
                "name": "Изобилие",
                "desc": "Энергия богатства и возможностей..."
            },
            "energy3": {
                "name": "Свет",
                "desc": "Энергия мудрости и гармонии..."
            }
        }
    except Exception as e:
        print("Ошибка в обработчике /get_rules:", e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/get_rule_text")
async def get_rule_text(
    chakra: str = Body(...),
    aspect: str = Body(...),
    value: int = Body(...)
):
    try:
        value_str = str(value)
        text = RULES["charkas"][chakra][aspect][value_str]
        return {"text": text}
    except Exception as e:
        print("Ошибка в обработчике /get_rule_text:", e)
        print(traceback.format_exc())
        return JSONResponse(status_code=404, content={"error": f"Нет описания для {chakra}/{aspect}/{value}: {e}"})

@app.get("/payments/compatibility-interpretation")
async def get_compatibility_result(order_id: str):
    """
    Получить результат совместимости по order_id (например, ORD-000123).
    """
    db = SessionLocal()
    try:
        # Извлекаем числовой id из строки вида ORD-000123
        id_int = int(order_id.replace("ORD-", ""))
        order = db.query(Order).filter(Order.id == id_int).first()
        if not order:
            return JSONResponse(status_code=404, content={"error": "Order not found"})
        if order.type != "compatibility":
            return JSONResponse(status_code=400, content={"error": "Order is not compatibility type"})
        if not order.compatibility_result:
            return JSONResponse(status_code=202, content={"message": "Result not ready yet"})
        return {"result": order.compatibility_result}
    finally:
        db.close()

@app.get("/payments/paid-interpretation")
async def get_personal_result(order_id: str):
    db = SessionLocal()
    try:
        id_int = int(order_id.replace("ORD-", ""))
        order = db.query(Order).filter(Order.id == id_int).first()
        if not order:
            return JSONResponse(status_code=404, content={"error": "Order not found"})
        if order.type != "personal":
            return JSONResponse(status_code=400, content={"error": "Order is not personal type"})
        if not order.personal_result:
            return JSONResponse(status_code=202, content={"message": "Result not ready yet"})
        return {"result": order.personal_result}
    finally:
        db.close()

@app.get("/payments/order-type")
async def get_order_type(order_id: str):
    db = SessionLocal()
    try:
        id_int = int(order_id.replace("ORD-", ""))
        order = db.query(Order).filter(Order.id == id_int).first()
        if not order:
            return JSONResponse(status_code=404, content={"error": "Order not found"})
        return {"type": order.type}
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)