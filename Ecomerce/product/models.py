from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.

CETEGORY_CHOICES = (
    ('St','strawberry'),
    ('Ba','banana'),
    ('Ap','apple'),
    ('Gua','guava'),
    ('Lem','lemon'),
    ('Fresh','fresh fruit'),
)
STATE_CHOICES = (
    ('N','Narowal'),
    ('D','Doday wali'),
    ('R','Ran'),
    ('C','Chaly wali'),
    ('R','Ransinwal'),
    ('K','Kharal'),
    ('Cl','Class goraya'),
    ('Ja','Jajo wali'),
    ('M','Mandra wala'),
)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    Name= models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=254, unique=True)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    zipcode = models.IntegerField(null=True,blank=True)
    state = models.CharField(choices=STATE_CHOICES, max_length=4)
    
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    class Meta:
        verbose_name = "Custom user"
        verbose_name_plural = "Custom users"

    def __str__(self):
        return self.get_full_name()

class Product(models.Model):
    name = models.CharField(max_length=70)
    title = models.CharField(max_length=70)
    price = models.IntegerField()
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    cetegory = models.CharField(choices=CETEGORY_CHOICES,max_length=6)
    description = models.TextField()
    image = models.ImageField(upload_to='upload/product')
    discounted_price = models.FloatField()

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cast(self):
        return self.quantity * self.product.price
    
STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('On the way','On the way'),
    ('Deliverd','Deliverd'),
    ('Cancel','Cancel'),
)
class Orderplaced(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_orderplaced')
    customer = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="Pending",choices=STATUS_CHOICES)


class News(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='upload/product/latest-news')

    def __str__(self):
        return str(self.title)

class ModelAdressModal(CustomUser):
    # address2 = models.CharField(max_length=254, blank=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name='address')


class Customer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Name = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=50)

    def __str__(self):
        return str(self.id)


class Contact(models.Model):
    name = models.CharField(max_length=254, blank=True)
    email = models.EmailField(max_length=254)
    phone = models.PositiveIntegerField()
    subject = models.CharField(max_length=254)
    message = models.TextField()

    def __str__(self):
        return str(self.name)


     