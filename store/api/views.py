from products.models import Category, Product, ShoppingCart
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .pagination import CustomPagination
from .serializers import CartSerializer, CategorySerializer, ProductSerializer


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


class ProductViewSet(ListViewSet):
    """Представление для модели Product."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ShoppingCartViewSet(ModelViewSet):
    """Представление для модели ShoppingCart."""

    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает корзину текущего пользователя.
        """
        return ShoppingCart.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        instance.cartitems.all().delete()
        instance.delete()

    @action(detail=True, methods=["post"])
    def clear(self, request, *args, **kwargs):
        """
        Очищает корзину текущего пользователя.
        """
        cart = self.get_object()
        cart.cart_items.all().delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
