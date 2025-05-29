import os
from django.core.asgi import get_asgi_application
from starlette.routing import Mount
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from api_service.main import app as fastapi_app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django_app = get_asgi_application()

# Определяем путь к статическим файлам
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
static_path = os.path.join(BASE_DIR, 'calculator', 'static')

routes = [
    # Маршрут для FastAPI-эндпоинтов
    Mount("/api", app=fastapi_app),
    # Маршрут для статики
    Mount("/static", app=StaticFiles(directory=os.path.join(BASE_DIR, 'calculator', 'static')), name="static"),
    Mount("/admin_static", app=StaticFiles(directory=os.path.join(BASE_DIR, 'venv', 'Lib', 'site-packages', 'django', 'contrib', 'admin', 'static')), name="admin_static"),
    # Остальные запросы передаются Django
    Mount("/", app=django_app),
]

application = Starlette(routes=routes)