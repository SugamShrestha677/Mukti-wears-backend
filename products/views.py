from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Product
from .serializers import ProductListSerializer, ProductDetailSerializer


class ProductListView(generics.ListAPIView):
    """List all active products. Supports ?category= and ?search= filtering."""

    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True)
        category = self.request.query_params.get("category")
        if category and category != "all":
            qs = qs.filter(category=category)
        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(name__icontains=search)
        return qs


class ProductDetailView(generics.RetrieveAPIView):
    """Retrieve a single product by slug."""

    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"
    queryset = Product.objects.filter(is_active=True)
