from django.db import models
from django.urls import reverse
from accounts.models import Profile

# Create your models here.


class ProductType(models.Model):
    # Only has a name and description for what the type of product is
    # IE: name should be something like "hat" or "keychain"
    name = models.CharField(max_length=255)
    description = models.TextField(default='')

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse('product_type', args=[str(self.pk)])

    def __str__(self):
        return self.name


class Product(models.Model):
    # subclass for status choices
    class ProductStatus(models.TextChoices):
        AVAILABLE = 'Available'
        ON_SALE = 'On Sale'
        OUT_OF_STOCK = 'Out of Stock'
    # for the actual product using the product type as a foreign key
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE,
                              related_name='product')
    image = models.ImageField(upload_to='images/', null=True)
    productType = models.ForeignKey(ProductType, on_delete=models.SET_NULL,
                                    null=True,
                                    related_name='product')
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField()
    status = models.CharField(max_length=50,
                              choices=ProductStatus.choices,
                              default=ProductStatus.AVAILABLE)

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse('merchstore:product-detail', args=[str(self.pk)])

    def __str__(self):
        return self.name


class Transaction(models.Model):
    # subclass for status choices
    class TransactionStatus(models.TextChoices):
        ON_CART = 'On Cart'
        TO_PAY = 'To Pay'
        TO_SHIP = 'To Ship'
        TO_RECEIVE = 'To Receive'
        DELIVERED = 'Delivered'
    buyer = models.ForeignKey(Profile, on_delete=models.SET_NULL,
                              null=True,
                              related_name='transaction')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='transaction')
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=50,
                              choices=TransactionStatus.choices)
    createdon = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('transaction', args=[str(self.pk)])

    def __str__(self):
        return self.product.name
