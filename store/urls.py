from . import views
from rest_framework_nested import routers


router = routers.DefaultRouter()  # type: ignore
router.register("product", views.ProductViewSet, basename="product")
router.register("collection", views.CollectionViewSet)
router.register("carts", views.CartViewSet)
router.register("customer", views.CustomerViewSet)
router.register("order", views.OrderViewSet)

product_router = routers.NestedDefaultRouter(router, "product", lookup="product")
product_router.register("review", views.ReviewViewSet, basename="product-review")

carts_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
carts_router.register("items", views.CartItemViewSet, basename="cart-items")

urlpatterns = router.urls + product_router.urls + carts_router.urls
