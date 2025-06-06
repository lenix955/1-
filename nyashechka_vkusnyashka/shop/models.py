from django.db import models
from django.contrib.auth.models import AbstractUser


# Пользователь
class User(AbstractUser):
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True, null=True)
    address = models.TextField(verbose_name="Адрес", blank=True, null=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.username} ({self.email})"


# Категория
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


# Магазин / Пекарня
class Store(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название магазина")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stores', verbose_name="Владелец")
    description = models.TextField(verbose_name="Описание", blank=True)
    address = models.TextField(verbose_name="Адрес")

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"

    def __str__(self):
        return self.name


# Товар
class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    name_en = models.CharField(max_length=200, verbose_name="Название (англ.)", blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Категория")
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products', verbose_name="Магазин")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name} ({self.price}₽)"


# Картинка товара
class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Товар")
    image = models.ImageField(upload_to='product_images/', verbose_name="Изображение")

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"

    def __str__(self):
        return f"Изображение для {self.product.name}"


# Акции / Промо
class Promotion(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название акции")
    description = models.TextField(verbose_name="Описание")
    products = models.ManyToManyField(Product, related_name='promotions', verbose_name="Товары")
    start_date = models.DateField(verbose_name="Начало")
    end_date = models.DateField(verbose_name="Окончание")

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"

    def __str__(self):
        return self.title
