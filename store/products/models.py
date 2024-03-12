from django.db import models


class Category(models.Model):
    """Модель категории товаров."""

    name = models.CharField(max_length=150, verbose_name="Наименование категории")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    image = models.ImageField(
        upload_to="media/categories/", help_text="Изображение категории"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


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

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ["name"]

    def __str__(self):
        return self.name


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

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name"]

    def __str__(self):
        return self.name
