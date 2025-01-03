from django.contrib import admin
from django.core.exceptions import ValidationError

from Makeover.models import Category, Order, OrderItem, Payment, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


class ProductsAdmin(admin.ModelAdmin):
    list_display = ["id", "short_name", "price", "stock", "category"]
    list_filter = ["category", "price"]
    search_fields = ["name", "category"]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('customer__first_name', 'customer__email')
    inlines = [OrderItemInline, PaymentInline]
    list_editable = ('status',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(payments__status='completed').distinct()


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    list_filter = ('order__status', 'product__category')
    search_fields = ('product__short_name', 'order__customer__first_name')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(order__payments__status='completed').distinct()


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'customer', 'amount', 'payment_id', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('payment_id', 'customer__first_name', 'order__id')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductsAdmin)

