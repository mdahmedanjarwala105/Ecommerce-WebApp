from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from django.contrib.auth import get_user_model
from store.models import (
    Product,
    Collection,
    Review,
    Cart,
    CartItem,
    Customer,
    Order,
    OrderItem,
)


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "inventory",
            "price",
            "tax_price",
            "collection",
        ]

    tax_price = serializers.SerializerMethodField(method_name="get_tax_price")

    def get_tax_price(self, product: Product):
        return product.price * Decimal(1.1)


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = [
            "id",
            "title",
            "product_count",
        ]

    product_count = serializers.IntegerField(read_only=True)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "id",
            "date",
            "name",
            "description",
        ]


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "price",
        ]


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(method_name="get_total_price")

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.price

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "quantity",
            "total_price",
        ]


class CartSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name="get_total_price")

    def get_total_price(self, cart: Cart):
        return sum(item.quantity * item.product.price for item in cart.items.all())  # type: ignore

    class Meta:
        model = Cart
        fields = [
            "id",
            "items",
            "total_price",
        ]


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Product does not exist.")
        return value

    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"]  # type: ignore
        quantity = self.validated_data["quantity"]  # type: ignore

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id,
                **self.validated_data,  # type: ignore
            )
        return self.instance

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product_id",
            "quantity",
        ]


class UpdateCartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = [
            "quantity",
        ]


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    def validate_user_id(self, value):
        User = get_user_model()
        if not User.objects.filter(pk=value).exists():
            raise serializers.ValidationError("User does not exist.")
        return value

    class Meta:
        model = Customer
        fields = [
            "id",
            "user_id",
            "phone",
            "birth_date",
            "membership",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "quantity",
        ]


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "customer", "placed_at", "payment_status", "items"]


class CreateOrderSerializer(serializers.ModelSerializer):

    cart_id = serializers.UUIDField()

    def save(self, **kwargs):
        with transaction.atomic():
            # Ensure that the order creation and cart deletion are atomic

            cart_id = self.validated_data["cart_id"]

            (customer, created) = Customer.objects.get_or_create(
                user_id=self.context["user_id"]
            )
            order = Order.objects.create(customer=customer)

            cart_item = CartItem.objects.select_related("product").filter(
                cart_id=cart_id
            )

            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    unit_price=item.product.price,
                    quantity=item.quantity,
                )
                for item in cart_item
            ]

            OrderItem.objects.bulk_create(order_items)

            Cart.objects.filter(pk=cart_id).delete()

            return order
