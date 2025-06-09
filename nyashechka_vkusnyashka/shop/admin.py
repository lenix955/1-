from django.contrib import admin
from django.db.models import Count
from .models import User, Category, Store, Product, Promotion, Order, OrderProduct, Review, CartItem

class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    fields = ('name', 'price', 'is_available')
    readonly_fields = ('name',)

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    fields = ('product', 'quantity', 'price')
    readonly_fields = ('product', 'price')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'date_joined', 'is_active')
    list_filter = ('is_active', 'date_joined')
    search_fields = ('username', 'email', 'phone')
    date_hierarchy = 'date_joined'
    readonly_fields = ('date_joined',)
    list_display_links = ('username', 'email')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count')
    search_fields = ('name', 'description')
    inlines = [ProductInline]

    @admin.display(description='Количество товаров')
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Количество товаров'

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'owner', 'product_count')
    list_filter = ('city', 'owner')
    search_fields = ('name', 'description', 'city', 'owner__username')
    raw_id_fields = ('owner',)
    inlines = [ProductInline]

    @admin.display(description='Количество товаров')
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Количество товаров'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'store', 'is_available', 'created_at')
    list_filter = ('category', 'store', 'is_available')
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    list_display_links = ('name',)
    raw_id_fields = ('category', 'store')

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'discount')
    list_filter = ('start_date', 'end_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'start_date'
    readonly_fields = ('start_date', 'end_date')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'delivery_address')
    date_hierarchy = 'created_at'
    inlines = [OrderProductInline]
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('user',)
    list_display_links = ('id',)

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__id', 'product__name')
    raw_id_fields = ('order', 'product')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'product__name', 'comment')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    raw_id_fields = ('user', 'product')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('user__username', 'product__name')
    date_hierarchy = 'added_at'
    readonly_fields = ('added_at',)
    raw_id_fields = ('user', 'product')