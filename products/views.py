from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .filters import ProductFilter


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    @extend_schema(
        parameters=[
            OpenApiParameter('title', OpenApiTypes.STR, description='Filter by title (case-insensitive substring)'),
            OpenApiParameter('sku', OpenApiTypes.STR, description='Filter by exact SKU'),
            OpenApiParameter('price_min', OpenApiTypes.DECIMAL, description='Minimum price (inclusive)'),
            OpenApiParameter('price_max', OpenApiTypes.DECIMAL, description='Maximum price (inclusive)'),
            OpenApiParameter('category', OpenApiTypes.INT, description='Category ID — includes all subcategories'),
        ],
        responses=ProductSerializer(many=True),
    )
    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
