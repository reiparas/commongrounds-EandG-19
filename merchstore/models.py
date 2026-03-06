from django.db import models

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
    # for the actual product using the product type as a foreign key
    name = models.CharField(max_length=255)
    productType = models.ForeignKey(ProductType, on_delete=models.SET_NULL,
                                    null=True,
                                    related_name='type')
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse('product', args=[str(self.pk)])

    def __str__(self):
        return self.name
