from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json
import datetime

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id}"
class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
    main_Icon=models.ImageField(upload_to='category_Icon/',null=True)

    def __str__(self):
        return f"{self.name}"
class Product(models.Model):
    name = models.CharField(max_length=100)
    user =models.ForeignKey(User,on_delete=models.CASCADE) # to know which user 
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    main_image=models.ImageField(upload_to='product_images/',null=True)
    product_group = models.ForeignKey('Category', on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name}"
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
class Winner(models.Model):
    auction = models.ForeignKey('Auction', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    winning_price = models.DecimalField(max_digits=10, decimal_places=2)
    win_date = models.DateTimeField(default=timezone.now)

def validate_future_date(value):
    if value.date() < timezone.now().date():
        raise ValidationError('The date should not be in the past.')

def validate_end_date(value):
    if value.date() < timezone.now().date():
        raise ValidationError('The end date should not be in the past.')

class Auction(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    auction_start_date = models.DateTimeField(default=timezone.now, validators=[validate_future_date])
    auction_end_date = models.DateTimeField(validators=[validate_end_date])
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    auction_status =     models.BooleanField(max_length=20, default=True)
    minimum_bid_increment = models.DecimalField(max_digits=10, decimal_places=2, default=1.0)
    created_at=models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return str(self.id)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.schedule_end_auction_task()

    def schedule_end_auction_task(self):
        from .tasks import end_auction_task
        from django_celery_beat.models import PeriodicTask, ClockedSchedule

        # إزالة المهام السابقة إذا كانت موجودة
        PeriodicTask.objects.filter(name=f'end-auction-task-{self.id}').delete()

        # إنشاء جدول زمنية جديد
        clocked_time = self.auction_end_date

        clocked_schedule, created = ClockedSchedule.objects.get_or_create(clocked_time=clocked_time)

        # إنشاء المهمة المجدولة
        PeriodicTask.objects.create(
            clocked=clocked_schedule,
            name=f'end-auction-task-{self.id}',
            task='auction.tasks.end_auction_task',
            args=json.dumps([self.id]),
            one_off=True
        )
        print('created success')

class Bid(models.Model):
    auction = models.ForeignKey(Auction, related_name='bids', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='bids', on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.id)
class AuctionRequest(models.Model):
    Auction = models.OneToOneField(Auction, on_delete=models.CASCADE , null=True,related_name='requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    admin_message = models.CharField(max_length=255 ,null=True)
    is_approved = models.BooleanField(null=True)
class Winner(models.Model):
    auction = models.ForeignKey('Auction', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    winning_bid = models.DecimalField(max_digits=10, decimal_places=2)
    win_date = models.DateTimeField(default=timezone.now)