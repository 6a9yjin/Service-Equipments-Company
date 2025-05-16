from django.db import models

# Create your models here.
class Register(models.Model):
    name = models.CharField(max_length=69)
    email = models.EmailField(unique=True)
    phone = models.IntegerField(null=True)
    password = models.CharField(max_length=69)
    age = models.IntegerField()
    gendchoices = (
        ('MALE','Male'),
        ('FEMALE','Female'),
    )
    gender = models.CharField(choices=gendchoices,max_length=69)
    address = models.CharField(max_length=200)

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'ELECTRONICS'),
        ('clothing', 'CLOTHING'),
        ('books', 'BOOKS'),
        ('furniture', 'FURNITURE'),
        ('food', 'FOOD'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    photo = models.FileField(upload_to='photo/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveBigIntegerField( null=True, blank=True)
    availability = models.BooleanField(default=True)

class Feedback(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    rating = models.IntegerField()  # From 1 to 5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} rated {self.product.name} ({self.rating} stars)"


class cart(models.Model):
    user=models.ForeignKey(Register,on_delete=models.CASCADE)
    products = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    total_price = models.IntegerField()

class Transaction(models.Model):
    user = models.ForeignKey(Register,on_delete=models.CASCADE)
    products = models.ForeignKey(Product,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveBigIntegerField(default=1)
    order_id = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)