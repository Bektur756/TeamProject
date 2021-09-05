from django.db import models
from hotels.models import Hotel
from django.contrib.auth import get_user_model


User = get_user_model()

STATUS_CHOICES = (
    ('prepaid', 'С предоплатой'),
    ('canceled', 'Отмененный'),
    ('finished', 'Завершенный')
)

class Reserve(models.Model):
    total_sum = models.DecimalField(max_digits=10,
                                    decimal_places=2,
                                    default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT,
                             related_name='reservations')
    status = models.CharField(max_length=20,
                              choices = STATUS_CHOICES,
                              default='prepaid')
    hotels = models.ManyToManyField(Hotel,
                                      through='ReserveItem')

    @property
    def total(self):
        items = self.items.values('hotel__price_per_day', 'quantity')
        total = 0
        for item in items:
            total += item['hotel__price_per_day'] * item['quantity']
        return total

    def __str__(self):
        return f'Бронь № {self.id} от {self.created_at.strftime("%d-%m-%Y %H:%M")}'

    class Meta:
        db_table = 'reserve'
        ordering = ['-created_at']


class ReserveItem(models.Model):
    reservation = models.ForeignKey(Reserve,
                              on_delete=models.RESTRICT,
                              related_name='items')
    hotel = models.ForeignKey(Hotel,
                                on_delete=models.RESTRICT,
                                related_name='reserve_items')
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        db_table = 'reserve_items'
    #class Meta для того, чтобы задать параметры общие, не касающиеся какого-то конкретного поля



