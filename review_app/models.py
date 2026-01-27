from django.db import models
from django.utils.text import slugify

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    image_url = models.URLField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    review_summary = models.TextField(blank=True, null=True)
    summary_updated_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name  


class Review(models.Model):
    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    author = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} ({self.rating} stars)"  
    




