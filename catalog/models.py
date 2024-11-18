from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Наименование категории")
    description = models.TextField(
        verbose_name="Описание категории", blank=True, null=True
    )

    class Meta:
        verbose_name = "Категория"  # Настройка для наименования одного объекта
        verbose_name_plural = "Категории"  # Настройка для наименования набора объектов
        ordering = ("name",)

    def __str__(self):
        # Строковое отображение объекта
        return f"{self.name} {self.description}"


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name="Наименование продукта")
    description = models.TextField(
        verbose_name="Описание продукта", blank=True, null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="сategories",
        blank=True,
        null=True,
    )
    photo = models.ImageField(
        upload_to="media/photo",
        blank=True,
        null=True,
        verbose_name="Изображение продукта",
    )
    price = models.IntegerField(verbose_name="Цена", blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, null=True, verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True, verbose_name="Дата последнего изменения"
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products", blank=True, null=True)
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')


    class Meta:
        verbose_name = "Продукт"  # Настройка для наименования одного объекта
        verbose_name_plural = "Продукты"  # Настройка для наименования набора объектов
        ordering = ("name",)
        permissions = [
            ("can_unpublish_product", 'Can unpublish product'),
            ("can_change_product_description", "Can change product description"),
            ("can_change_product_category", "Can change product category"),
        ]

    def __str__(self):
        # Строковое отображение объекта
        return f"{self.name} {self.category} {self.price}"


class Version(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="versions",
        verbose_name="product",
    )
    version_number = models.CharField(max_length=50, verbose_name="Номер версии")
    version_name = models.CharField(max_length=150, verbose_name="Название версии")
    is_current = models.BooleanField(
        default=False, verbose_name="Признак текущей версия"
    )

    class Meta:
        verbose_name = "Версия продукта"
        verbose_name_plural = "Версии продукта"
        ordering = ["product"]

    def __str__(self):
        return f"{self.product.name} - {self.version_name} ({self.version_number})"
