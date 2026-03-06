from django.db import models

# Create your models here.


class ProductType(models.Model):
    name = models.CharField(255)
    description = models.TextField

    def get_absolute_url(self):
        return reverse('product_type', args=[str(self.pk)])


class Product(models.Model):
    name = models.CharField(255)
    productType = models.ForeignKey(ProductType, on_delete=models.SET_NULL, 
                                    relatedname='type')
    description = models.TextField()
    price = models.DecimalField(decimal_places=2)

    def get_absolute_url(self):
        return reverse('product', args=[str(self.pk)])