from rest_framework import serializers

from .models import Cart, CartItems
from catalog_api.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price"]


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)
    sub_total = serializers.SerializerMethodField(method_name="total")

    class Meta:
        model = CartItems
        fields = ["id", "cart", "product", "quantity", "sub_total"]

    def total(self, cartitem: CartItems):
        return cartitem.quantity * cartitem.product.price


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                "There is no product associated with the given ID")

        return value

    def validate(self, data):
        # ... other validations (like product_id check) ...

        product = Product.objects.get(pk=data['product_id'])
        cart = Cart.objects.get(pk=self.context["cart_id"])  # Access the cart

        # Combined quantity check
        new_quantity = data.get('quantity', 1)  # Default to 1 if not in data
        existing_quantity = cart.items.filter(product=product).first()
        existing_quantity = existing_quantity.quantity if existing_quantity else 0

        if new_quantity + existing_quantity > product.stock:
            raise serializers.ValidationError("Not enough stock available.")

        return data

    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]

        try:
            cartitem = CartItems.objects.get(
                product_id=product_id, cart_id=cart_id)
            cartitem.quantity += quantity
            cartitem.save()

            self.instance = cartitem

        except:
            self.instance = CartItems.objects.create(
                cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItems
        fields = ["id", "product_id", "quantity"]


class UpdateCartItemSerializer(serializers.ModelSerializer):

    def validate_quantity(self, value):
        cartitem = self.instance
        product = cartitem.product
        if value > product.stock:
            raise serializers.ValidationError("Insufficient stock.")
        return value

    class Meta:
        model = CartItems
        fields = ["quantity"]


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    grand_total = serializers.SerializerMethodField(method_name='main_total')

    class Meta:
        model = Cart
        fields = ["id", "items", "grand_total"]

    def main_total(self, cart: Cart):
        items = cart.items.all()
        total = sum([item.quantity * item.product.price for item in items])
        return total
