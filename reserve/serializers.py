from rest_framework import serializers

from .models import Reserve, ReserveItem

class ReserveItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReserveItem
        exclude = ('id', 'reservation')


class ReserveSerializer(serializers.ModelSerializer):
    items = ReserveItemSerializer(many=True)
    created_at = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)


    class Meta:
        model = Reserve
        exclude = ('user', 'hotels')


    def create(self, validated_data):
        request = self.context.get('request')
        items = validated_data.pop('items')
        user = request.user
        reservation = Reserve.objects.create(user=user)
        total = 0
        for item in items:
            total += item['hotel'].price_per_day * item['quantity']
            ReserveItem.objects.create(reservation=reservation,
                                     hotel=item['hotel'],
                                     quantity=item['quantity'])
        reservation.total_sum = total
        reservation.save()
        return reservation







