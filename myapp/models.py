from django.contrib.auth.models import AbstractUser
from django.db import models

# User Table (Customer + Admin)
class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return f"{self.username} ({self.role})"


# Product Table
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    specifications = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    image_url = models.CharField(max_length=200, blank=True)  # simple string for image
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name


# Order Table (with Shipping Address)
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'customer'})
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, default="Pending")
    delivery_status = models.CharField(max_length=20, default="Processing")

    # Shipping Address
    shipping_address = models.TextField()
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"Order {self.id} by {self.customer.username}"


# Order Details Table
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


# Payment Table
class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)  # eSewa, Khalti, Mobile Banking
    transaction_id = models.CharField(max_length=100)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, default="Pending")


# Review Table
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'customer'})
    rating = models.IntegerField()  # 1 to 5 stars
    comment = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} - {self.rating}⭐"