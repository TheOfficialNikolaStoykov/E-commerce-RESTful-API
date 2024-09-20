from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .serializers import *

# BRAND

@api_view(["GET"])
def list_brands_view(request):
    brands = Brand.objects.all()
    
    serializer = BrandSerializer(brands, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_brand_view(request):
    serializer = BrandSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def retrieve_single_brand_view(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    
    serializer = BrandSerializer(brand)
    return Response(serializer.data)
    
@api_view(["PUT", "PATCH"])
@permission_classes([IsAdminUser])
def edit_brand_view(request, pk):
    if request.method == "PUT":
        brand = get_object_or_404(Brand, pk=pk)
        serializer = BrandSerializer(brand, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "PATCH":
        brand = get_object_or_404(Brand, pk=pk)
        serializer = BrandSerializer(brand, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_brand_view(request, pk):       
    brand = get_object_or_404(Brand, pk=pk)
    brand.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# CATEGORY

@api_view(["GET"])
def list_categories_view(request):
    categories = Category.objects.all()
    
    serializer = CategorySerializer(categories, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_category_view(request):
    serializer = CategorySerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def retrieve_single_category_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    serializer = CategorySerializer(category)
    return Response(serializer.data)
    
@api_view(["PUT", "PATCH"])
@permission_classes([IsAdminUser])
def edit_category_view(request, pk):
    if request.method == "PUT":
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "PATCH":
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_category_view(request, pk):       
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# PRODUCT

class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["category__name", "brand__name"]
    search_filters = ["name"]
    
@api_view(["GET"])
def list_products_view(request):
    products = Product.objects.all()
    
    serializer = ProductSerializer(products, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_product_view(request):
    serializer = ProductSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def retrieve_single_product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    serializer = ProductSerializer(product)
    return Response(serializer.data)
    
@api_view(["PUT", "PATCH"])
@permission_classes([IsAdminUser])
def edit_product_view(request, pk):
    if request.method == "PUT":
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "PATCH":
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_product_view(request, pk):       
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
    

# PRODUCT REVIEW

@api_view(["GET"])
def list_reviews_view(request):
    reviews = ProductReview.objects.all()
    
    serializer = ProductReviewSerializer(reviews, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_review_view(request):
    serializer = ProductReviewSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def retrieve_single_review_view(request, pk):
    review = get_object_or_404(ProductReview, pk=pk)
    
    serializer = ProductReviewSerializer(review)
    return Response(serializer.data)
    
@api_view(["PUT", "PATCH"])
@permission_classes([IsAdminUser])
def edit_review_view(request, pk):
    if request.method == "PUT":
        review = get_object_or_404(ProductReview, pk=pk)
        serializer = ProductReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "PATCH":
        review = get_object_or_404(ProductReview, pk=pk)
        serializer = ProductReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_review_view(request, pk):       
    review = get_object_or_404(ProductReview, pk=pk)
    review.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)