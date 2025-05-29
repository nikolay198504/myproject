from django.urls import path
from . import views

app_name = 'calculator'

urlpatterns = [
    path('', views.calc, name='calc'),  # Главная страница калькулятора
    path('payment-success', views.payment_success, name='payment_success'),  # Страница успеха после оплаты
    path('create_order/', views.create_order, name='create_order'),
]