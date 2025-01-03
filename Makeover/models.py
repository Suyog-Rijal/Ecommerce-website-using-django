import uuid

from django.db import models
from django.utils import timezone

from Authentication.models import UserModel


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    
class Product(models.Model):
    short_name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=500, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    primary_image = models.ImageField(upload_to='static/products/', blank=True, null=True)
    optionalImage_1 = models.ImageField(upload_to='static/products/', blank=True, null=True)
    optionalImage_2 = models.ImageField(upload_to='static/products/', blank=True, null=True)
    stock = models.PositiveIntegerField()
    express_delivery = models.BooleanField(default=False)
    rating = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name='products')

    def __str__(self):
        return self.short_name

    def get_discounted_price(self):
        return self.price - (self.price * self.discount_percent / 100)


class Order(models.Model):
    id = models.CharField(max_length=8, primary_key=True, editable=False, unique=True)
    customer = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('shipped', 'Shipped'),
                 ('delivered', 'Delivered'), ('canceled', 'Canceled')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:
            current_time = timezone.now()
            self.id = current_time.strftime("%y%m%d%H%M%S")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.order.id}"


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    customer = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('completed', 'Completed'),
                 ('failed', 'Failed'), ('refunded', 'Refunded')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment #{self.payment_id} for Order #{self.order.id} by {self.customer.first_name} - Status: {self.status}"

    def add_reward_points(self, reward_percent=0):
        if self.status == 'completed':
            points_to_add = int(self.amount * reward_percent)
            self.customer.reward_points += points_to_add
            self.customer.save()

        return 0