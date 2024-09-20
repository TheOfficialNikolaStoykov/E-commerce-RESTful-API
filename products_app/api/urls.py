from django.urls import path

from .views import *

urlpatterns = [
    # BRAND
    path("brands/view/all/", list_brands_view, name="brands"),
    path("brands/view/<int:pk>/", retrieve_single_brand_view, name="brand"),
    path("brands/create/", create_brand_view, name="brand-create"),
    path("brands/edit/<int:pk>/", edit_brand_view, name="brand-edit"),
    path("brands/delete/<int:pk>/", delete_brand_view, name="brand-delete"),
    
    # CATEGORY
    path("categories/view/all/", list_categories_view, name="categories"),
    path("categories/view/<int:pk>/", retrieve_single_category_view, name="category"),
    path("categories/create/", create_category_view, name="category-create"),
    path("categories/edit/<int:pk>/", edit_category_view, name="category-edit"),
    path("categories/delete/<int:pk>/", delete_category_view, name="category-delete"),
    
    # PRODUCT
    path("view/all/", ProductListView.as_view(), name="products"),
    path("view/<int:pk>/", retrieve_single_product_view, name="product"),
    path("create/", create_product_view, name="product-create"),
    path("edit/<int:pk>/", edit_product_view, name="product-edit"),
    path("delete/<int:pk>/", delete_product_view, name="product-delete"),
    
    # PRODUCT REVIEW
    path("reviews/view/all/", list_reviews_view, name="reviews"),
    path("reviews/view/<int:pk>/", retrieve_single_product_view, name="review"),
    path("reviews/create/", create_review_view, name="review-create"),
    path("reviews/edit/<int:pk>/", edit_review_view, name="review-edit"),
    path("reviews/delete/<int:pk>/", delete_review_view, name="review-delete")
]