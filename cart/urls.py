from django.urls import path, include
from .views import CartViewSet, CartItemViewSet

from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers


router = routers.DefaultRouter()

router.register("carts", CartViewSet)
cart_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
cart_router.register("items", CartItemViewSet, basename="cart-items")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(cart_router.urls)),
]
app_name = 'cart'
