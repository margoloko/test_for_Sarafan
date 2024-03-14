from django.db import models
from users.models import CustomUser as User


class Category(models.Model):
    """Модель категории товаров."""

    name = models.CharField(max_length=150, verbose_name="Наименование категории")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    image = models.ImageField(
        upload_to="media/categories/", help_text="Изображение категории"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]


class SubCategory(models.Model):
    """Модель подкатегории товаров."""

    name = models.CharField(max_length=150, verbose_name="Наименование подкатегории")
    slug = models.SlugField(unique=True)
    image = models.ImageField(
        upload_to="media/subcategories/", verbose_name="Изображение подкатегории"
    )
    category = models.ForeignKey(
        Category, related_name="subcategories", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ["name"]


class Product(models.Model):
    """Модель продуктов."""

    name = models.CharField(max_length=200, verbose_name="Наименование продукта")
    slug = models.SlugField(unique=True)
    image_small = models.ImageField(
        upload_to="products/small/",
        verbose_name="Маленькое изображение продукта",
        help_text="Изображение продукта в маленьком размере",
    )
    image_medium = models.ImageField(
        upload_to="media/products/medium/",
        verbose_name="Среднее изображение",
        help_text="Изображение продукта в среднем размере",
    )
    image_large = models.ImageField(
        upload_to="media/products/large/",
        verbose_name="Большое изображение",
        help_text="Изображение продукта в большом размере",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    subcategory = models.ForeignKey(
        SubCategory,
        related_name="products",
        on_delete=models.CASCADE,
        verbose_name="Подкатегория продукта",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name"]


class ShoppingCart(models.Model):
    """Модель корзины пользователя."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="shopping_cart"
    )
    product = models.ManyToManyField(
        Product,
        through="ShoppingCartItems",
        related_name="cart",
    )

    def __str__(self):
        return f"Корзина товаров {self.user}"

    class Meta:
        verbose_name = "Корзина"


class ShoppingCartItems(models.Model):
    """Модель продуктов в корзине."""

    cart = models.ForeignKey(
        ShoppingCart, on_delete=models.CASCADE, related_name="cart_items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name}: {self.quantity} шт."
