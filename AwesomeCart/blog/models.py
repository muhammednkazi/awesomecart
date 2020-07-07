from django.db import models

# Create your models here.
class Blogpost(models.Model):
    post_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=50)
    category=models.CharField(max_length=500,default="")
    heading0=models.CharField(max_length=500,default="")
    content0=models.CharField(max_length=5000,default="")
    heading1=models.CharField(max_length=500,default="")
    content1=models.CharField(max_length=5000,default="")
    pub_date=models.DateTimeField()
    thumbnail=models.ImageField(upload_to="blog/images",default="")

    # this function displays title on the table rows.
    def __str__(self):
        return self.title