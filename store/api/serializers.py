from products.models import Category, Product, SubCategory
from rest_framework.serializers import ModelSerializer, StringRelatedField


class SubCategorySerializer(ModelSerializer):
    """
    Сериализатор для вывода информации о категориях и подкатегориях в ProductSerializer.
    """

    category = StringRelatedField(read_only=True)

    class Meta:
        model = SubCategory
        fields = [
            "name",
            "category",
        ]


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

    subcategory = SubCategorySerializer(read_only=True)

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
        ]
