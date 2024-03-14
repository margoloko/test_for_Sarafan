from products.models import Category, Product, ShoppingCart, ShoppingCartItems
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .pagination import CustomPagination
from .serializers import (
    AddItemSerializer,
    CartItemSerializer,
    CartSerializer,
    CategorySerializer,
    ProductSerializer,
)


class ListViewSet(ListModelMixin, GenericViewSet):
    """
    Базовый класс вьюсета.
    Возвращает список объектов (для обработки запросов GET).
    """

    pagination_class = CustomPagination


class CategoryViewSet(ListViewSet):
    """Представление для просмотра списка категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(ListViewSet):
    """Представление для просмотра продуктов."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ShoppingCartViewSet(ListModelMixin, GenericViewSet):
    """Представление для просмотра корзины пользователя и очищения корзины."""

    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Возвращает корзину текущего пользователя."""
        return ShoppingCart.objects.filter(user=self.request.user)

    @action(detail=True, methods=["post"])
    def clear(self, request, *args, **kwargs):
        """Очищает корзину текущего пользователя."""
        cart = self.get_object()
        cart.cart_items.all().delete()
        return Response(
            {"message": "Корзина очищена"}, status=status.HTTP_204_NO_CONTENT
        )


class ShoppingCartItemsViewSet(ModelViewSet):
    """Представление для управления элементами корзины текущего пользователя."""

    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Возвращает элементы корзины текущего пользователя."""
        return ShoppingCartItems.objects.filter(cart__user=self.request.user)


class AddItemsView(generics.CreateAPIView):
    """Представление для добавления товаров в корзину."""

    queryset = ShoppingCartItems.objects.all()
    serializer_class = AddItemSerializer
    permission_classes = [IsAuthenticated]
