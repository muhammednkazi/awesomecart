from django.db import models
# here we create databse tables with their columns and column datatype.

# Create your models here.
# table product
class product(models.Model):
    product_id=models.AutoField
    product_name=models.CharField(max_length=50)
    category=models.CharField(max_length=50,default="")
    sub_category=models.CharField(max_length=50,default="")
    desc=models.CharField(max_length=300)
    pub_date=models.DateField()
    price=models.IntegerField(default=0)
    image=models.ImageField(upload_to="shop/images",default="")

    # this function displays product names on the table rows.
    def __str__(self):
        return self.product_name

# table contactus
class contactus_table(models.Model):
    msg_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=70,default="")
    phone=models.CharField(max_length=15,default="")
    email=models.CharField(max_length=70,default="")
    desc=models.TextField(max_length=500,default="")
    timestamp=models.DateTimeField(auto_now_add=True,blank = True)

    # this function displays customer's name on the table rows.
    def __str__(self):
        return self.name


# table contactus
class Order(models.Model):
    order_id=models.AutoField(primary_key=True)
    items_json=models.CharField(max_length=5000,default="")
    amount=models.IntegerField(default=0)
    name=models.CharField(max_length=100,default="")
    email=models.CharField(max_length=100,default="")
    address=models.CharField(max_length=500,default="")
    city=models.CharField(max_length=70,default="")
    state=models.CharField(max_length=100,default="")
    zip_code=models.CharField(max_length=15,default="")
    phone=models.CharField(max_length=15,default="")

    # this function displays customer's name on the table rows.
    def __str__(self):
        return self.name

class OrderUpdate(models.Model):
    update_id=models.AutoField(primary_key=True)
    order_id=models.IntegerField(default="")
    update_desc=models.CharField(max_length=5000)
    timestamp=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."
    