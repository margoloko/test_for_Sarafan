from products.models import Category, Product, SubCategory
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from .pagination import CustomPagination
from .serializers import CategorySerializer, ProductSerializer, SubCategorySerializer


class ListViewSet(ListModelMixin, GenericViewSet):
    """
    Базовый класс вьюсета.
    Возвращает список объектов (для обработки запросов GET).
    """

    pagination_class = CustomPagination


class CategoryViewSet(ListViewSet):
    """Представление для модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryViewSet(ListViewSet):
    """Представление для модели SubCategory."""

    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class ProductViewSet(ListViewSet):
    """Представление для модели Product."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
