from django.contrib.auth import  get_user_model
from django.db import models

User = get_user_model()


class Hotel(models.Model):
    hotel_name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images',
                              null=True,
                              blank=True)

    class Meta:
        ordering = ['hotel_name', 'price_per_day']

    def __str__(self):
        return self.hotel_name


class HotelReview(models.Model):
    hotel = models.ForeignKey(Hotel,
                                on_delete=models.CASCADE,
                                related_name='reviews')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='reviews')

    text = models.TextField()
    likes = models.BooleanField(default=False)
    rating = models.SmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

# fuser -k 8000/tcp