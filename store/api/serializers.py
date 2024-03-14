from products.models import Category, Product, ShoppingCart, ShoppingCartItems
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    StringRelatedField,
)


class CategorySerializer(ModelSerializer):
    """Сериализатор для модели Category."""

    subcategories = StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            "name",
            "slug",
            "image",
            "subcategories",
        ]


class ProductSerializer(ModelSerializer):
    """Сериализатор для модели Product."""

    category = StringRelatedField(source="subcategory.category.name")
    subcategory = StringRelatedField(source="subcategory.name")

    class Meta:
        model = Product
        fields = [
            "name",
            "slug",
            "image_small",
            "image_medium",
            "image_large",
            "price",
            "subcategory",
            "category",
        ]


class CartItemsSerializer(ModelSerializer):
    """Сериализатор для вывода информации о продуктах и количестве в CartSerializer."""

    product = StringRelatedField()

    class Meta:
        model = ShoppingCartItems
        fields = ["product", "quantity"]


class CartSerializer(ModelSerializer):
    """Сериализатор для модели ShoppingCart."""

    cart_items = CartItemsSerializer(many=True, read_only=True)
    total_cost = SerializerMethodField()
    total_quantity = SerializerMethodField()

    class Meta:
        model = ShoppingCart
        fields = ["cart_items", "total_cost", "total_quantity"]

    def get_total_cost(self, obj):
        """
        Вычисляет общую стоимость товаров в корзине.

        Возвращает:
            float: Общая стоимость товаров в корзине.
        """
        return sum(item.product.price * item.quantity for item in obj.cart_items.all())

    def get_total_quantity(self, obj):
        """
        Вычисляет общее количество товаров в корзине.

        Возвращает:
            int: Общее количество товаров в корзине.
        """
        return sum(item.quantity for item in obj.cart_items.all())
