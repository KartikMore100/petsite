from django.db import models
from django.db.models import Manager


class customanager(models.Manager):
    def getdata(self,a):
        return super().get_queryset().filter(species = a)
    
# Create your models here.
class Pet(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    species = models.CharField(max_length=100)
    breeds = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = (('Male', 'male'),('Female','female'))
    gender = models.CharField(max_length=100, choices = gender)
    image = models.ImageField(upload_to="media")
    price = models.FloatField()
    slug = models.SlugField(default='', null=False)

    cpetobj = customanager()
    objects = Manager()

    class Meta:
        db_table = 'Pet'


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phoneno = models.BigIntegerField()
    password = models.CharField(max_length=200)
    wishlist = models.ManyToManyField(Pet, related_name='wishlist_customers', blank=True)

    class Meta:
        db_table = 'Customer'

class Cart(models.Model):
    cid = models.ForeignKey(Customer, on_delete=models.CASCADE)
    pid = models.ForeignKey(Pet, on_delete=models.CASCADE)
    quanity = models.IntegerField()
    totalamount = models.FloatField()

    class Meta:
        db_table = 'cart'


class Order(models.Model):
    ordernumber = models.CharField(max_length=100)
    orderdate = models.DateField(max_length=100)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phoneno = models.BigIntegerField()
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state  = models.CharField(max_length=100)
    pincode = models.BigIntegerField(max_length=100)
    orderstatus = models.CharField(max_length=100)

    class Meta:
        db_table = 'Order'

        
class Payment(models.Model):
    customerid = models.ForeignKey(Customer, on_delete= models.CASCADE)
    oid = models.ForeignKey(Order,on_delete= models.CASCADE)
    paymentstatus = models.CharField(max_length= 100, default= 'pending')
    transactionid = models.CharField(max_length=200)
    paymentmode = models.CharField(max_length= 100, default= 'paypal')

    class Meta:
        db_table = 'Payment'


class Orderdetail(models.Model):
    ordernumber = models.CharField(max_length= 100)
    customerid = models.ForeignKey(Customer,on_delete= models.CASCADE)
    productid = models.ForeignKey(Pet, on_delete= models.CASCADE)
    quantity = models.IntegerField()
    totalprice = models.IntegerField()
    paymentid = models.ForeignKey(Payment, on_delete= models.CASCADE, null=True)
    created_at = models.DateField(auto_now= True)
    updated_at = models.DateField(auto_now= True)

    class Meta:
        db_table = 'Orderdetail'