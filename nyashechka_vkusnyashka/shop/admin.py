from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import (
    User, Category, Store, Product, Image, Promotion
)

@admin.display(description="Роли")
def display_roles(obj):
    return ", ".join(group.name for group in obj.groups.all())

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', display_roles)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    readonly_fields = ('date_joined', 'last_login')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {
            'fields': ('phone', 'address')
        }),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'address')
    search_fields = ('name', 'owner__username')
    list_filter = ('owner',)

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    readonly_fields = ('image_preview',)

    @admin.display(description='Превью')
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 50px;" />', obj.image.url)
        return "—"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'store', 'price', 'created_at')
    list_filter = ('category', 'store', 'created_at')
    search_fields = ('name', 'description')
    inlines = [ImageInline]


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date')
    filter_horizontal = ('products',)
    search_fields = ('title', 'description')
    list_filter = ('start_date', 'end_date')
