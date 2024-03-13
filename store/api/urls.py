from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ProductViewSet, ShoppingCartViewSet

router = DefaultRouter()

router.register(r"categories", CategoryViewSet)
router.register(r"products", ProductViewSet, basename="product")
router.register(r"cart", ShoppingCartViewSet, basename="cart")

urlpatterns = [
    path("", include(router.urls)),
]
