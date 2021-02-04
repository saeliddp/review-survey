from django.db import models

# Create your models here.

class Respondent(models.Model):
    position = models.PositiveSmallIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    product_seq = models.CharField(max_length=100, default="None")
    mturk_id = models.CharField(max_length=50, default="None")
    factors = models.CharField(max_length=255, default="None")
    additional = models.CharField(max_length=255, default="None")

class Product(models.Model):
    name = models.CharField(max_length=210, default="None")
    amazon_id = models.CharField(max_length=50, default="None")
    description = models.CharField(max_length=800, default="None")
    review1 = models.CharField(max_length=130, default="None")
    review2 = models.CharField(max_length=130, default="None")
    review3 = models.CharField(max_length=130, default="None")
    num_responses = models.PositiveSmallIntegerField(default=0)

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    respondent = models.ForeignKey(Respondent, on_delete=models.CASCADE)
    review1_rating = models.PositiveSmallIntegerField(default=0)
    review2_rating = models.PositiveSmallIntegerField(default=0)
    review3_rating = models.PositiveSmallIntegerField(default=0)
    time_elapsed = models.PositiveSmallIntegerField(default=0)