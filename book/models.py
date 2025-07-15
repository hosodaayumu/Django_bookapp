from django.db import models
from .consts import MAX_RATE


RATE_CHOICES = [(x, str(x)) for x in range(0, MAX_RATE + 1)]

CATEGORY = (
    ('ビジネス', 'ビジネス'),
    ('生活', '生活'),
    ('趣味', '趣味'),
    ('漫画', '漫画'),
    ('その他', 'その他'),
)

class Shelf(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    
    category = models.CharField(
        max_length=100,
        choices = CATEGORY,
        )
    thumbnail = models.ImageField(null=True, blank=True)
    def __str__(self):
        return self.title

class Review(models.Model):
    book = models.ForeignKey(Shelf, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    rate = models.IntegerField(choices=RATE_CHOICES)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

# Create your models here.


