from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="subcategories",
    )

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} -> {self.name}"
        return self.name


class CakeSize(models.Model):
    CAKE_SIZE_CHOICES = [
        ("8_inch_round", "8 inch Round"),
        ("10_inch_round", "10 inch Round"),
        ("12_inch_round", "12 inch Round"),
        ("8_inch_square", "8 inch Square"),
        ("10_inch_square", "10 inch Square"),
        ("12_inch_square", "12 inch Square"),
    ]

    name = models.CharField(
        max_length=50,
        choices=CAKE_SIZE_CHOICES,
        unique=True,  # Prevent duplicate sizes
    )
    description = models.TextField(blank=True, null=True)  # Optional details
    price = models.DecimalField(max_digits=6, decimal_places=2)  # Price for this size

    def __str__(self):
        return f"{self.get_name_display()} - €{self.price}"


class Cake(models.Model):
    OCCASION_CHOICES = [
        ("wedding", "Wedding"),
        ("birthday", "Birthday"),
        ("anniversary", "Anniversary"),
        ("baby_shower", "Baby Shower"),
        ("gender_reveal", "Gender Reveal"),
        ("communion", "Communion"),
        ("confirmation", "Confirmation"),
        ("christening", "Christening"),
        ("other", "Other"),
    ]
    occasion = models.CharField(
        max_length=50, choices=OCCASION_CHOICES, default="other"
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    sizes = models.ManyToManyField(
        CakeSize, related_name="cakes"
    )  # Multiple sizes per cake
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = CloudinaryField("image", blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="cakes"
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class CustomCake(models.Model):
    FLAVOR_CHOICES = [
        ("vanilla", "Vanilla"),
        ("chocolate", "Chocolate"),
        ("red_velvet", "Red Velvet"),
        ("lemon", "Lemon"),
        ("carrot", "Carrot"),
    ]

    FILLING_CHOICES = [
        ("chocolate", "Chocolate"),
        ("buttercream", "Buttercream"),
        ("raspberry", "Raspberry"),
        ("lemon", "Lemon"),
        ("cream_cheese", "Cream Cheese"),
    ]

    flavor = models.CharField(max_length=50, choices=FLAVOR_CHOICES, default="vanilla")
    filling = models.CharField(
        max_length=50, choices=FILLING_CHOICES, default="buttercream"
    )
    inscription = models.CharField(max_length=255, blank=True, null=True)
    sizes = models.ManyToManyField(CakeSize, related_name="custom_cakes", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = CloudinaryField("image", blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return f"Custom Cake - {self.flavor} with {self.filling} filling"


class Product(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ("cake", "Cake"),
        ("cupcake", "Cupcake"),
        ("other", "Other"),
    ]

    product_type = models.CharField(
        max_length=50, choices=PRODUCT_TYPE_CHOICES, default="cake"
    )
    name = models.CharField(max_length=255)
    preview_description = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="products",
        null=True,
        blank=True,
    )
    image = CloudinaryField("image", blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
