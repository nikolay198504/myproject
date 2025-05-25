from django.db import models

class Order(models.Model):
    status = models.CharField(max_length=50, default="pending")
    date = models.CharField(max_length=50, blank=True, null=True)
    points = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)
    customer_email = models.EmailField(blank=True, null=True)
    paid_at = models.DateTimeField(blank=True, null=True)  # дата и время оплаты

    def __str__(self):
        return f"{self.order_id} ({self.status})"

    @property
    def order_id(self):
        return f"ORD-{self.id:06d}"

    class Meta:
        managed = True  # или просто удали эту строку — по умолчанию True
        db_table = 'orders'
