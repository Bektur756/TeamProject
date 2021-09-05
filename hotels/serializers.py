from rest_framework import serializers
from .models import Hotel, HotelReview


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ('id', 'hotel_name', 'price_per_day')


class HotelDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ('id', 'hotel_name', 'description', 'price_per_day', 'image', 'reviews')


class CreateHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError('Цена не может быть отрицательной')
        return price


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = HotelReview
        fields = ('id', 'author', 'hotel_name', 'text', 'rating', 'created_at')

    def validate_hotel(self, hotel):
        request = self.context.get('request')
        user = request.user
        if self.Meta.model.objects.filter(hotel=hotel, author=user).exists():
            raise serializers.ValidationError('Вы уже оставляли отзыв вчера')
        return hotel

    def validate_rating(self, rating):
        if rating not in range(1, 6):
            raise serializers.ValidationError('Рейтинг может быть от одного до 5')
        return rating

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = request.user
        return super().create(validated_data)