from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = [
        ("men", "Men"),
        ("women", "Women"),
        ("accessories", "Accessories"),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    description = models.TextField()
    story = models.TextField(blank=True)
    care = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=10)
    image = models.URLField(max_length=500, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    series = models.CharField(max_length=100, blank=True)
    sizes = models.JSONField(default=list)
    colours = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
