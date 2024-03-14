from products.models import Category, Product, ShoppingCart, ShoppingCartItems
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    IntegerField,
    ModelSerializer,
    PrimaryKeyRelatedField,
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
    """Сериализатор информации о продуктах и количестве."""

    product = StringRelatedField()

    class Meta:
        model = ShoppingCartItems
        fields = ["id", "product", "quantity"]


class CartSerializer(ModelSerializer):
    """Сериализатор информации о корзине."""

    cart_items = CartItemsSerializer(many=True, read_only=True)
    total_cost = SerializerMethodField()
    total_quantity = SerializerMethodField()

    class Meta:
        model = ShoppingCart
        fields = ["id", "cart_items", "total_cost", "total_quantity"]

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


class CartItemSerializer(ModelSerializer):
    """Сериализатор для элементов корзины."""

    class Meta:
        model = ShoppingCartItems
        fields = ["product", "quantity"]


class AddItemSerializer(ModelSerializer):
    """Сериализатор для добавления товара в корзину."""

    product_id = PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = IntegerField(default=1)

    class Meta:
        model = ShoppingCartItems
        fields = ["quantity", "product_id"]

    def create(self, validated_data):
        """Добавление товара в корзину."""
        user = self.context["request"].user
        product_id = validated_data.get("product_id").id
        quantity = validated_data.get("quantity")
        shopping_cart, created = ShoppingCart.objects.get_or_create(user=user)
        if ShoppingCartItems.objects.filter(
            cart=shopping_cart, product_id=product_id
        ).exists():
            raise ValidationError("Товар уже находится в корзине")
        shopping_cart_item = ShoppingCartItems.objects.create(
            cart=shopping_cart, product_id=product_id, quantity=quantity
        )
        return shopping_cart_item
