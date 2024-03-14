from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AddItemsView,
    CategoryViewSet,
    ProductViewSet,
    ShoppingCartItemsViewSet,
    ShoppingCartViewSet,
)

router = DefaultRouter()

router.register(r"categories", CategoryViewSet)
router.register(r"products", ProductViewSet, basename="product")
router.register(r"cart", ShoppingCartViewSet, basename="cart")
router.register(r"cart/items", ShoppingCartItemsViewSet, basename="cartitem")

urlpatterns = [
    path("", include(router.urls)),
    path("shopping_cart/add/", AddItemsView.as_view(), name="add"),
]
