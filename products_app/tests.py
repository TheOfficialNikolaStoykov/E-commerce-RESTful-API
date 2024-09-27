from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import *


class BrandTestCase(APITestCase):
    """
    Test case for brand-related endpoints.
    """

    def setUp(self):
        """
        Set up test data including users and brand.
        """
        self.admin_user = User.objects.create_superuser(username="test_admin_user", password="password")
        self.user = User.objects.create_user(username="test_user", password="password")
        self.brand = Brand.objects.create(name="Test", description="Test")
     
    def test_brand_list(self):
        """
        Test listing all brands.
        """
        response = self.client.get(reverse("brands"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_brand_create_unauthenticated(self):
        """
        Test creating a brand as an unauthenticated user.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        
        data = {
            "name": "Test",
            "description": "Test"
        }
        response = self.client.post(reverse("brand-create"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_brand_edit_unauthenticated(self):
        """
        Test editing a brand as an unauthenticated user.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        
        data = {
            "name": "Test",
            "description": "Test"
        }
        response = self.client.put(reverse("brand-edit", args=(self.brand.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_brand_delete_unauthenticated(self):
        """
        Test deleting a brand as an unauthenticated user.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        
        response = self.client.delete(reverse("brand-delete", args=(self.brand.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_brand_create_admin(self):
        """
        Test creating a brand as an admin user.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        data = {
            "name": "Test",
            "description": "Test"
        }
        response = self.client.post(reverse("brand-create"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_brand_create_admin_400(self):
        """
        Test creating a brand with invalid data as an admin.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        data = {
            "test": "Test"
        }
        response = self.client.post(reverse("brand-create"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_brand_edit_put_admin_200(self):
        """
        Test editing a brand using PUT as an admin.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)
        
        data = {
            "name": "Test - edited",
            "description": "Test"
        }
        response = self.client.put(reverse("brand-edit", args=(self.brand.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_brand_edit_put_admin_400(self):
        """
        Test editing a brand with invalid data using PUT as an admin.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)
        
        data = {
            "test": "Test"
        }
        response = self.client.put(reverse("brand-edit", args=(self.brand.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_brand_edit_patch_admin(self):
        """
        Test editing a brand using PATCH as an admin.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)
        
        data = {
            "name": "Test - edited",
            "description": "Test - edited"
        }
        response = self.client.patch(reverse("brand-edit", args=(self.brand.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_brand_delete_admin(self):
        """
        Test deleting a brand as an admin user.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        response = self.client.delete(reverse("brand-delete", args=(self.brand.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_retrieve_single_brand(self):
        """
        Test retrieving a single brand by its ID.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        
        response = self.client.get(reverse("brand", args=(self.brand.id,)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CategoryTestCase(APITestCase):
    """
    Test case for category-related endpoints.
    """

    def setUp(self):
        """
        Set up test data including users and category.
        """
        self.admin_user = User.objects.create_superuser(username="test_admin_user", password="password")
        self.user = User.objects.create_user(username="test_user", password="password")
        self.category = Category.objects.create(name="Test Category", description="Test Description")
    
    def test_category_list(self):
        """
        Test listing all categories.
        """
        response = self.client.get(reverse("categories"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_category_create_unauthenticated(self):
        """
        Test creating a category as an unauthenticated user.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        data = {"name": "New Category", "description": "New Category Description"}
        response = self.client.post(reverse("category-create"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_category_create_admin_201(self):
        """
        Test creating a category as an admin user.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        data = {"name": "New Category", "description": "New Category Description"}
        response = self.client.post(reverse("category-create"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_category_create_admin_400(self):
        """
        Test creating a category with invalid data as an admin.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        data = {"name": ""}
        
        response = self.client.post(reverse("category-create"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_category_edit_admin_put(self):
        """
        Test editing a category using PUT as an admin.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        data = {"name": "Test", 
                "description": "Test"
        }
         
        response = self.client.put(reverse("category-edit", args=(self.category.id,)), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_category_edit_admin_patch_200(self):
        """
        Test editing a category using PATCH as an admin.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        data = {
            "name": "Test - Edited",
            "description": "Updated Description"
        }
         
        response = self.client.patch(reverse("category-edit", args=(self.category.id,)), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_category_edit_admin_patch_400(self):
        """
        Test editing a category with invalid data using PATCH as an admin.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        data = {
            "name": "",
        }
         
        response = self.client.put(reverse("category-edit", args=(self.category.id,)), data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_category_delete_admin(self):
        """
        Test deleting a category as an admin user.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        response = self.client.delete(reverse("category-delete", args=(self.category.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_category_delete_unauthenticated(self):
        """
        Test deleting a category as an unauthenticated user.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.delete(reverse("category-delete", args=(self.category.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_retrieve_single_category(self):
        """
        Test retrieving a single category by its ID.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
         
        response = self.client.get(reverse("category", args=(self.category.id,)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProductTestCase(APITestCase):
    """
    Test case for product-related endpoints.
    """

    def setUp(self):
        """
        Set up test data including users, brand, category, and product.
        """
        self.admin_user = User.objects.create_superuser(username="test_admin_user", password="password")
        self.user = User.objects.create_user(username="test_user", password="password")
        self.brand = Brand.objects.create(name="Test Brand", description="Test Brand Description")
        self.category = Category.objects.create(name="Test Category", description="Test Category Description")
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Product Description",
            price=99.99,
            stock=50,
            category=self.category,
            brand=self.brand
        )
        
    def test_product_list(self):
        """
        Test listing all products.
        """
        response = self.client.get(reverse("products"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_product_create_unauthenticated(self):
        """
        Test creating a product as an unauthenticated user.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        data = {
            "name": "New Product",
            "description": "New Product Description",
            "price": 99.99,
            "stock": 10,
            "category": self.category.id,
            "brand": self.brand.id,
        }
        response = self.client.post(reverse("product-create"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_product_create_admin_201(self):
        """
        Test creating a product as an admin user.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        new_brand = Brand.objects.create(name="New Brand", description="New Brand Description")
        
        data = {
            "name": "New Product",
            "description": "New Product Description",
            "price": 99.99,
            "stock": 10,
            "category": self.category.id,
            "brand": new_brand.id,
        }

        response = self.client.post(reverse("product-create"), data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_product_edit_admin_put_200(self):
        """
        Test editing a product using PUT as an admin.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        data = {
            "name": "Test",
            "description": "Updated Description",
            "price": 99.99,
            "stock": 20,
            "category": self.category.id,
            "brand": self.brand.id
        }

        response = self.client.put(reverse("product-edit", args=(self.product.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_product_create_admin_400(self):
        """
        Test creating a product with invalid data as an admin.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)
        
        data = {
            "test": "Test",
        }

        response = self.client.post(reverse("product-create"), data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_product_edit_admin_patch_200(self):
        """
        Test editing a product using PATCH as an admin.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        data = {
            "name": "Test - Edited",
        }
         
        response = self.client.patch(reverse("product-edit", args=(self.product.id,)), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_product_edit_admin_patch_400(self):
        """
        Test editing a product with invalid data using PATCH as an admin.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        data = {
            "name": "",
        }
         
        response = self.client.put(reverse("product-edit", args=(self.product.id,)), data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_product_delete_admin(self):
        """
        Test deleting a product as an admin user.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        response = self.client.delete(reverse("product-delete", args=(self.product.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_retrieve_single_product(self):
        """
        Test retrieving a single product by its ID.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.get(reverse("product", args=(self.product.id,)))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProductReviewTestCase(APITestCase):
    """
    Test case for product review-related endpoints.
    """

    def setUp(self):
        """
        Set up test data including users, brand, category, product, and review.
        """
        self.admin_user = User.objects.create_superuser(username="test_admin_user", password="password")
        self.user = User.objects.create_user(username="test_user", password="password")
        self.brand = Brand.objects.create(name="Test Brand", description="Test Brand Description")
        self.category = Category.objects.create(name="Test Category", description="Test Category Description")
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Product Description",
            price=99.99,
            stock=50,
            category=self.category,
            brand=self.brand
        )
        self.review = ProductReview.objects.create(product=self.product, user=self.user, rating=5, description="Great product!")
    
    def test_review_list(self):
        """
        Test listing all product reviews.
        """
        response = self.client.get(reverse("reviews"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_review_create_admin(self):
        """
        Test creating a product review as an admin user.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        data = {
            "product": self.product.id,
            "user": self.user.id,
            "rating": 4,
            "description": "Test product"
        }
        
        response = self.client.post(reverse("review-create"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_review_create_admin_400(self):
        """
        Test creating a product review with invalid data as an admin.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)
        
        data = {
            "product": "",
        }

        response = self.client.post(reverse("review-create"), data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_edit_admin(self):
        """
        Test editing a product review as an admin user.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        data = {
            "product": self.product.id,
            "user": self.user.id,
            "rating": 3,
            "description": "Updated description"
        }
        
        response = self.client.put(reverse("review-edit", args=(self.review.id,)), data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_delete_admin(self):
        """
        Test deleting a product review as an admin user.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        response = self.client.delete(reverse("review-delete", args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_retrieve_single_review(self):
        """
        Test retrieving a single product review by its ID.
        """
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.get(reverse("review", args=(self.product.id,)))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_review_edit_admin_patch_200(self):
        """
        Test editing a product review using PATCH as an admin.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        data = {
            "rating": 1,
        }
         
        response = self.client.patch(reverse("product-edit", args=(self.product.id,)), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_review_edit_admin_patch_400(self):
        """
        Test editing a product review with invalid data using PATCH as an admin.
        """
        self.client.login(username=self.admin_user.username, password=self.admin_user.password)
        self.token_admin = Token.objects.get(user__username=self.admin_user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_admin.key)

        data = {
            "rating": "",
        }
         
        response = self.client.patch(reverse("review-edit", args=(self.product.id,)), data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)