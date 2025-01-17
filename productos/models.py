from django.db import models
from django.contrib.auth.models import User


def some_function():
    from productos.models import Product 

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='', blank=True, null=True)
    technical_specs = models.TextField()
    category = models.CharField(max_length=100, default="General") 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def reduce_stock(self, quantity):
        if self.stock >= quantity:
            
            self.stock -= quantity
            self.save()
            return True
        return False

    class Meta:
        permissions = [
            ("can_manage_products", "Puede gestionar productos"),
        ]

    def __str__(self):  
        return self.name


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.product.name} - {self.purchased_at}"
