from django.contrib import admin
from . import models
from django.db.models import QuerySet
from django.db.models.aggregates import Count
from django.utils.html import format_html
from urllib.parse import urlencode
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.admin import ModelAdmin


class InventoryFilter(admin.SimpleListFilter):
    title = "Inventory"
    parameter_name = "inventory"

    def lookups(
        self, request: HttpRequest, model_admin: ModelAdmin
    ) -> list[tuple[str, str]]:
        return [("<10", "Low"), (">=10", "OK")]

    def queryset(self, request: HttpRequest, queryset: QuerySet):
        if self.value() == "<10":
            return queryset.filter(inventory__lt=10)
        if self.value() == ">=10":
            return queryset.filter(inventory__gte=10)


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    readonly_fields = ["thumbnail"]
    extra = 0
    min_num = 1
    max_num = 10

    # def thumbnail(self, instance: models.ProductImage):
    #     if instance.image.name != "":
    #         return format_html(f'<img src = "{instance.image.url}" class="thumbnail"/>')
    #     return ""

    def thumbnail(self, instance: models.ProductImage):
        if instance.image.name != "":
            return format_html('<img src="{}" class="thumbnail"/>', instance.image.url)
        return ""


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ["title__istartswith"]
    autocomplete_fields = ["collection"]
    prepopulated_fields = {"slug": ("title",)}
    actions = ["clear_inventory"]
    inlines = [ProductImageInline]
    list_display = ["title", "price", "inventory_status", "collection_title"]
    list_editable = ["price"]
    list_per_page = 10
    list_select_related = ["collection"]
    list_filter = ["collection", "last_update", InventoryFilter]

    def collection_title(self, product: models.Product):
        return product.collection

    @admin.display(ordering="inventory")
    def inventory_status(self, product: models.Product):
        if product.inventory < 10:
            return "Low"
        return "OK"

    @admin.action(description="Clear inventory")
    def clear_inventory(self, request: HttpRequest, queryset: QuerySet):
        updated_count = queryset.update(inventory=0)
        self.message_user(request, f"{updated_count} products were updated.")

    class Media:
        css = {"all": ["store/style.css"]}


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "membership", "orders_count"]
    list_editable = ["membership"]
    list_select_related = ["user"]
    ordering = ["user__first_name", "user__last_name"]
    list_per_page = 10
    search_fields = ["user__first_name__istartswith", "user__last_name__istartswith"]

    @admin.display(ordering="orders_count")
    def orders_count(self, customer: models.Customer):
        url = (
            reverse("admin:store_order_changelist")
            + "?"
            + urlencode({"customer__id": customer.id})
        )
        return format_html('<a href="{}">{}</a>', url, customer.orders_count)

    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).annotate(orders_count=Count("order"))


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 0
    min_num = 1
    max_num = 10
    autocomplete_fields = ["product"]


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    autocomplete_fields = ["customer"]
    list_display = ["id", "placed_at", "customer"]


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title", "products_count"]
    search_fields = ["title__istartswith"]

    @admin.display(ordering="products_count")
    def products_count(self, collection: models.Collection):
        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({"collection__id": collection.id})
        )
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).annotate(products_count=Count("products"))
