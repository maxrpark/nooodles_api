from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(default='', null=False, unique=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(default='', null=False, unique=True)

    def __str__(self):
        return self.name


class SpicyLevel(models.Model):
    level = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.level


class Tags (models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Noodle(models.Model):
    name = models.CharField(max_length=250)
    summary = models.TextField(blank=True)
    instructions = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags)
    ingredients = models.ManyToManyField(Ingredient)
    spicy_level = models.ForeignKey(SpicyLevel, on_delete=models.CASCADE)
    amount_per_package = models.IntegerField()
    price_per_package = models.DecimalField(max_digits=6, decimal_places=2,         validators=[
        MinValueValidator(0),
        MaxValueValidator(100)
    ])
    price_per_unite = models.DecimalField(max_digits=6, decimal_places=2, validators=[
        MinValueValidator(0),
        MaxValueValidator(100)
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(default='', null=False, unique=True)
    rating = models.IntegerField(default=0, validators=[
        MinValueValidator(0),
        MaxValueValidator(5)
    ])

    def __str__(self):
        return self.name


class NoodleImage(models.Model):
    noodle = models.ForeignKey(Noodle, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='noodles_api/')
    created_at = models.DateTimeField(auto_now_add=True)
