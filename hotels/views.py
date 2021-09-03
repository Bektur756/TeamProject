from django.http import HttpResponse
from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters

from .models import Hotel, HotelReview
# from product.permissions import IsAuthorOrIsAdmin
from .serializers import (HotelSerializer, HotelDetailsSerializer,
                                  CreateHotelSerializer, ReviewSerializer)


def test_view(request):
    return HttpResponse('Hello World!')

@api_view(['GET'])
def hotel_list(request):
    hotels = Hotel.objects.all()

    # [product], [product2], [product3]
    serializer = HotelSerializer(hotels, many=True)
    # {id : 1 , title : 2}
    return Response(serializer.data)


class HotelFilter(filters.FilterSet):
    price_from = filters.NumberFilter('price_per_day', 'gte')
    price_to = filters.NumberFilter('price_per_day', 'lte')

    class Meta:
        model = Hotel
        fields = ('price_from', 'price_to')


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    filter_backends = [filters.DjangoFilterBackend,
                       rest_filters.SearchFilter,
                       rest_filters.OrderingFilter]
    # filterset_fields = ('price_per_day')
    filterset_class = HotelFilter
    search_fields = ['hotel_name', 'description']
    ordering_fields = ['hotel_name', 'price_per_day']

    def get_serializer_class(self):
        if self.action == 'list':
            return HotelSerializer
        elif self.action == 'retrieve':
            return HotelDetailsSerializer
        return CreateHotelSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAdminUser()]
        return []

#api/v1/product/id/reviews
    @action(['GET'], detail=True)
    def reviews(self, request, pl=None):
        hotel = self.get_object()
        reviews = hotel.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=200)


#Создает только залогиненный пользователь
# Редактировать или удалять может либо админ, либо автор

class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = HotelReview.objects.all()
    serializer_class = ReviewSerializer