from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from drf_spectacular.utils import OpenApiResponse, extend_schema_view, extend_schema

from .serializers import *


# BRAND

@extend_schema(
    responses={200: BrandSerializer(many=True)},
    description="List all brands."
)
@api_view(["GET"])
def list_brands_view(request):
    """
    List all brands.
    """
    brands = Brand.objects.all()
    
    serializer = BrandSerializer(brands, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    request=BrandSerializer,
    responses={
        201: BrandSerializer,
        400: OpenApiResponse(description="Bad Request")
    },
    description="Create a new brand. Admin only."
)
@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_brand_view(request):
    """
    Create a new brand.
    """
    serializer = BrandSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={200: BrandSerializer},
    description="Retrieve a single brand by ID."
)
@api_view(["GET"])
def retrieve_single_brand_view(request, pk):
    """
    Retrieve a single brand by ID.
    """
    brand = get_object_or_404(Brand, pk=pk)
    
    serializer = BrandSerializer(brand)
    return Response(serializer.data)


@extend_schema(
    request=BrandSerializer,
    responses={200: BrandSerializer, 400: OpenApiResponse(description="Bad Request")},
    description="Edit a brand. Admin only."
)
@api_view(["PUT", "PATCH"])
@permission_classes([IsAdminUser])
def edit_brand_view(request, pk):
    """
    Edit a brand (PUT or PATCH).
    """
    brand = get_object_or_404(Brand, pk=pk)

    if request.method == "PUT":
        serializer = BrandSerializer(brand, data=request.data)
    else:
        serializer = BrandSerializer(brand, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={204: None},
    description="Delete a brand. Admin only."
)
@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_brand_view(request, pk):
    """
    Delete a brand.
    """
    brand = get_object_or_404(Brand, pk=pk)
    brand.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# CATEGORY

@extend_schema(
    responses={200: CategorySerializer(many=True)},
    description="List all categories."
)
@api_view(["GET"])
def list_categories_view(request):
    """
    List all categories.
    """
    categories = Category.objects.all()
    
    serializer = CategorySerializer(categories, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    request=CategorySerializer,
    responses={
        201: CategorySerializer,
        400: OpenApiResponse(description="Bad Request")
    },
    description="Create a new category. Admin only."
)
@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_category_view(request):
    """
    Create a new category.
    """
    serializer = CategorySerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={200: CategorySerializer},
    description="Retrieve a single category by ID."
)
@api_view(["GET"])
def retrieve_single_category_view(request, pk):
    """
    Retrieve a single category by ID.
    """
    category = get_object_or_404(Category, pk=pk)
    
    serializer = CategorySerializer(category)
    return Response(serializer.data)


@extend_schema(
    request=CategorySerializer,
    responses={200: CategorySerializer, 400: OpenApiResponse(description="Bad Request")},
    description="Edit a category. Admin only."
)
@api_view(["PUT", "PATCH"])
@permission_classes([IsAdminUser])
def edit_category_view(request, pk):
    """
    Edit a category (PUT or PATCH). Admin only.
    """
    category = get_object_or_404(Category, pk=pk)

    if request.method == "PUT":
        serializer = CategorySerializer(category, data=request.data)
    else:
        serializer = CategorySerializer(category, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={204: None},
    description="Delete a category. Admin only."
)
@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_category_view(request, pk):
    """
    Delete a category.
    """
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# PRODUCT

@extend_schema_view(
    list=extend_schema(
        responses={200: ProductSerializer(many=True)},
        description="List all products with filtering and search capabilities."
    )
)
class ProductListView(ListAPIView):
    """
    List all products with filtering and search capabilities.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["category__name", "brand__name"]
    search_filters = ["name"]


@extend_schema(
    responses={200: ProductSerializer(many=True)},
    description="List all products."
)
@api_view(["GET"])
def list_products_view(request):
    """
    List all products.
    """
    products = Product.objects.all()
    
    serializer = ProductSerializer(products, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    request=ProductSerializer,
    responses={
        201: ProductSerializer,
        400: OpenApiResponse(description="Bad Request")
    },
    description="Create a new product. Admin only."
)
@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_product_view(request):
    """
    Create a new product.
    """
    serializer = ProductSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={200: ProductSerializer},
    description="Retrieve a single product by ID."
)
@api_view(["GET"])
def retrieve_single_product_view(request, pk):
    """
    Retrieve a single product by ID.
    """
    product = get_object_or_404(Product, pk=pk)

    serializer = ProductSerializer(product)
    return Response(serializer.data)


@extend_schema(
    request=ProductSerializer,
    responses={200: ProductSerializer, 400: OpenApiResponse(description="Bad Request")},
    description="Edit a product. Admin only."
)
@api_view(["PUT", "PATCH"])
@permission_classes([IsAdminUser])
def edit_product_view(request, pk):
    """
    Edit a product (PUT or PATCH). Admin only.
    """
    product = get_object_or_404(Product, pk=pk)

    if request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data)
    else:
        serializer = ProductSerializer(product, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={204: None},
    description="Delete a product. Admin only."
)
@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_product_view(request, pk):
    """
    Delete a product.
    """
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# PRODUCT REVIEW

@extend_schema(
    responses={200: ProductReviewSerializer(many=True)},
    description="List all product reviews."
)
@api_view(["GET"])
def list_reviews_view(request):
    """
    List all product reviews.
    """
    reviews = ProductReview.objects.all()
    
    serializer = ProductReviewSerializer(reviews, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    request=ProductReviewSerializer,
    responses={
        201: ProductReviewSerializer,
        400: OpenApiResponse(description="Bad Request")
    },
    description="Create a new product review. Admin only."
)
@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_review_view(request):
    """
    Create a new product review.
    """
    serializer = ProductReviewSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={200: ProductReviewSerializer},
    description="Retrieve a single product review by ID."
)
@api_view(["GET"])
def retrieve_single_review_view(request, pk):
    """
    Retrieve a single product review by ID.
    """
    review = get_object_or_404(ProductReview, pk=pk)
    
    serializer = ProductReviewSerializer(review)
    return Response(serializer.data)


@extend_schema(
    request=ProductReviewSerializer,
    responses={200: ProductReviewSerializer, 400: OpenApiResponse(description="Bad Request")},
    description="Edit a product review. Admin only."
)
@api_view(["PUT", "PATCH"])
@permission_classes([IsAdminUser])
def edit_review_view(request, pk):
    """
    Edit a product review (PUT or PATCH). Admin only.
    """
    review = get_object_or_404(ProductReview, pk=pk)

    if request.method == "PUT":
        serializer = ProductReviewSerializer(review, data=request.data)
    else:
        serializer = ProductReviewSerializer(review, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={204: None},
    description="Delete a product review. Admin only."
)
@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_review_view(request, pk):
    """
    Delete a product review.
    """
    review = get_object_or_404(ProductReview, pk=pk)
    review.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)