from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from .managers import CustomUserManager


class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """
    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("username"), max_length=50)
    email = LowercaseEmailField(_('email address'), unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # if you require phone number field in your project
    phone_regex = RegexValidator( regex = r'^\d{10}$',message = "phone number should exactly be in 10 digits")
    phone = models.CharField(max_length=255, validators=[phone_regex], blank = True, null=True)  # you can set it unique = True
    house = models.CharField(max_length=255,blank = True, null=True)
    area = models.CharField(max_length=255,blank = True, null=True)
    landmark = models.CharField(max_length=255,blank = True, null=True)
    pincode = models.CharField(max_length=6,blank = True, null=True)
    town = models.CharField(max_length=255,blank = True, null=True)
    state = models.CharField(max_length=255,blank = True, null=True)
    country = models.CharField(max_length=255,blank = True, null=True)
  



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    def __str__(self):
        return self.username
    #place here
        # if not the code below then taking default value in User model not in proxy models
    
    
class Collection(models.Model):
    category = models.CharField(max_length=30)
    image = models.ImageField(upload_to='base/images', default="")
    color = models.CharField(max_length=8)
    
    def __str__(self):
        return self.category

class Prodtype(models.Model):
    product = models.CharField(max_length=10)

    def __str__(self):
        return self.product  

    
class Store(models.Model):
    prod_name = models.CharField(max_length=30)
    prod_price =  models.PositiveIntegerField(default=0)
    image1 = models.ImageField(upload_to='images/',default="")
    image2 = models.ImageField(upload_to='images/',default="")
    image3 = models.ImageField(upload_to='images/',default="")
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    prodtype = models.ForeignKey(Prodtype, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.prod_name
    
class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    razor_pay_order_id = models.CharField(max_length=100,null=True,blank=True)
    razor_pay_payment_id = models.CharField(max_length=100,null=True,blank=True)
    razor_pay_payment_signature = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Store, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.prod_name} in Cart "



class Order(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    razor_pay_order_id = models.CharField(max_length=100,null=True,blank=True)
    razor_pay_payment_id = models.CharField(max_length=100,null=True,blank=True)
    razor_pay_payment_signature = models.CharField(max_length=100,null=True,blank=True)
    ord_prod = models.ManyToManyField(Store)
    created = models.DateTimeField(default=timezone.now)
    

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f"{self.user}Order{self.razor_pay_order_id} "