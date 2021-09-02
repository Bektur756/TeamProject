from django.http import HttpResponse
from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters

from hotels.models import Product, ProductReview
from product.permissions import IsAuthorOrIsAdmin
from product.serializers import (ProductSerializer, ProductDetailsSerializer,
                                 CreateProductSerializer, ReviewSerializer)


def test_view(request):
    return HttpResponse('Hello World!')

@api_view(['GET'])
def products_list(request):
    products = Product.objects.all()

    # [product], [product2], [product3]
    serializer = ProductSerializer(products, many=True)
    # {id : 1 , title : 2}
    return Response(serializer.data)

# class ProductsListView(APIView):
#     def get(self, request):
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)
#
# class ProductsListView(ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
# class ProductsDetailsView(RetrieveAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductDetailsSerializer
#
# class CreateProductView(CreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = CreateProductSerializer
#
# class UpdateProductView(UpdateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = CreateProductSerializer
#
# class DeleteProductView(DestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = CreateProductSerializer

class ProductFilter(filters.FilterSet):
    price_from = filters.NumberFilter('price', 'gte')
    price_to = filters.NumberFilter('price', 'lte')
    class Meta:
        model = Product
        fields = ('price_from', 'price_to')

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    filter_backends = [filters.DjangoFilterBackend,
                       rest_filters.SearchFilter,
                       rest_filters.OrderingFilter]
    # filterset_fields = ('price')
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'price']

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     print(queryset)
    #     print(self.request.query_params)
    #     price_from = self.request.query_params.get('price_from')
    #     price_to = self.request.query_params.get('price_to')
    #     queryset = queryset.filter(price__gte=price_from, price__lte=price_to)
    #     return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductSerializer
        elif self.action == 'retrieve':
            return ProductDetailsSerializer
        return CreateProductSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAdminUser()]
        return []

    #api/v1/product/id/reviews
    @action(['GET'], detail=True)
    def reviews(self, request, pl=None):
        product = self.get_object()
        reviews = ProductReview.objexts.filter(product=product)
        reviews = product.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=200)

#Создает только залогиненный пользователь
# Редактировать или удалять может либо админ, либо автор

class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAuthorOrIsAdmin()]
        return []