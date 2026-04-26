from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from products.models import Category, Product


class ProductSearchTests(APITestCase):
    def setUp(self):
        self.electronics = Category.objects.create(name='Electronics')
        self.phones = Category.objects.create(name='Phones', parent=self.electronics)
        self.clothing = Category.objects.create(name='Clothing')

        self.phone = Product.objects.create(
            title='Smartphone X',
            sku='PHN-001',
            price='599.99',
            category=self.phones,
        )
        self.laptop = Product.objects.create(
            title='Laptop Pro',
            sku='LAP-001',
            price='1299.99',
            category=self.electronics,
        )
        self.shirt = Product.objects.create(
            title='Blue Shirt',
            sku='SHT-001',
            price='29.99',
            category=self.clothing,
        )
        self.url = reverse('product-search')

    def test_search_by_title(self):
        res = self.client.get(self.url, {'title': 'smart'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        skus = [p['sku'] for p in res.data]
        self.assertIn('PHN-001', skus)
        self.assertNotIn('LAP-001', skus)

    def test_search_by_sku(self):
        res = self.client.get(self.url, {'sku': 'LAP-001'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['sku'], 'LAP-001')

    def test_filter_by_price_range(self):
        res = self.client.get(self.url, {'price_min': '100', 'price_max': '700'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        skus = [p['sku'] for p in res.data]
        self.assertIn('PHN-001', skus)
        self.assertNotIn('LAP-001', skus)
        self.assertNotIn('SHT-001', skus)

    def test_filter_by_category_includes_descendants(self):
        # Filtering by 'Electronics' should return both the laptop and the phone (child category)
        res = self.client.get(self.url, {'category': self.electronics.pk})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        skus = [p['sku'] for p in res.data]
        self.assertIn('PHN-001', skus)
        self.assertIn('LAP-001', skus)
        self.assertNotIn('SHT-001', skus)

    def test_filter_by_leaf_category(self):
        res = self.client.get(self.url, {'category': self.phones.pk})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        skus = [p['sku'] for p in res.data]
        self.assertIn('PHN-001', skus)
        self.assertNotIn('LAP-001', skus)

    def test_no_filters_returns_all(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)

    def test_combined_filters(self):
        res = self.client.get(self.url, {'category': self.electronics.pk, 'price_max': '700'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        skus = [p['sku'] for p in res.data]
        self.assertIn('PHN-001', skus)
        self.assertNotIn('LAP-001', skus)
